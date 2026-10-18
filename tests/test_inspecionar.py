"""Testes do inspetor com um vídeo sintético gerado pelo próprio ffmpeg (sem baixar nada)."""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills" / "revisar-video" / "scripts"))
import inspecionar  # noqa: E402

pytestmark = pytest.mark.skipif(not shutil.which("ffmpeg"), reason="precisa de ffmpeg")


@pytest.fixture(scope="module")
def video(tmp_path_factory):
    """6 s: 3 s vermelho + 3 s azul (um corte brusco em 3 s), com um tom de áudio."""
    pasta = tmp_path_factory.mktemp("v")
    arq = pasta / "teste.mp4"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-f", "lavfi", "-i", "testsrc2=size=360x640:rate=30:duration=3,hue=h=0",
                    "-f", "lavfi", "-i", "testsrc2=size=360x640:rate=30:duration=3,hue=h=180",
                    "-f", "lavfi", "-i", "sine=frequency=440:duration=6",
                    "-filter_complex", "[0:v][1:v]concat=n=2:v=1[v]", "-map", "[v]", "-map", "2:a",
                    "-shortest", str(arq)], check=True)
    return arq


def test_info_video(video):
    info = inspecionar.info_video(video)
    assert info["largura"] == 360 and info["altura"] == 640
    assert 5.5 < info["duracao_s"] < 6.5
    assert info["tem_audio"]


def test_cenas_do_roteiro_com_duracao():
    roteiro = {"cenas": [{"narracao": "um dois", "dur_s": 2}, {"narracao": "tres", "dur_s": 4}]}
    cenas = inspecionar.fronteiras(roteiro, [], 6.0)
    assert [(a, b) for a, b, _ in cenas] == [(0.0, 2.0), (2.0, 6.0)]


def test_cenas_pelos_cortes_sem_roteiro():
    cenas = inspecionar.fronteiras(None, [3.0], 6.0)
    assert [(a, b) for a, b, _ in cenas] == [(0.0, 3.0), (3.0, 6.0)]


def test_comparar_narracao_ignora_acentos_e_numeros():
    r = inspecionar.comparar_narracao("A bola passa de duzentos por hora", "a bola passa de 200 por hora")
    assert r["divergencias"] == [] and r["erros"] == []
    r = inspecionar.comparar_narracao("o olho acompanha", "o olho companha")
    assert r["divergencias"] == [{"roteiro": "acompanha", "ouvido": "companha"}]


def test_comparar_narracao_separa_erro_de_suspeita():
    r = inspecionar.comparar_narracao("o olho acompanha a bola", "o olho companha a bola")
    assert r["suspeitas"] == [{"roteiro": "acompanha", "ouvido": "companha"}] and r["erros"] == []
    r = inspecionar.comparar_narracao("o olho acompanha a bola", "o olho acompanha mancinhas a bola", duvidosas=["bola"])
    assert r["erros"] == [{"roteiro": "", "ouvido": "mancinhas"}] and r["duvidosas"] == ["bola"]
    assert inspecionar.comparar_narracao("ela contrai a pupila", "ela acasse a pupila")["erros"]   # palavra trocada
    assert inspecionar.comparar_narracao("essas correntes empurram", "correntes empurram")["erros"]   # engolida
    r = inspecionar.comparar_narracao("correntes de ar poderosas que a transportam", "correntes de arpoderosas que transportam")
    assert r["erros"] == [] and [s["ouvido"] for s in r["suspeitas"]] == ["arpoderosas", ""]   # emenda e "a" engolido


def test_main_gera_medidas_e_folhas(video, tmp_path):
    saida = tmp_path / "out"
    assert inspecionar.main([str(video), "--saida", str(saida)]) == 0
    medidas = json.loads((saida / "medidas.json").read_text(encoding="utf-8"))
    assert medidas["video"]["altura"] == 640
    assert medidas["audio"]["lufs_integrado"] is not None
    assert medidas["folhas"] == ["folha_1.jpg"]           # 6 s cabem numa folha de 12 s
    assert (saida / "folha_1.jpg").stat().st_size > 1000
    assert len(medidas["cenas"]) >= 1


def test_video_inexistente(tmp_path):
    assert inspecionar.main([str(tmp_path / "nao_existe.mp4")]) == 2


def _audio(tmp_path, nome, filtro):
    arq = tmp_path / nome
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i", filtro, str(arq)],
                   check=True)
    return arq


def _analisar(arq, narracao=None):
    log = inspecionar._ffmpeg(["-i", str(arq), "-af", "ebur128=peak=true,silencedetect=n=-45dB:d=0.7",
                               "-f", "null", "-"])
    info = {"duracao_s": float(re.findall(r"Duration: (\d+):(\d+):([\d.]+)", log)[0][2]), "audio_hz": 48000, "audio_canais": 1}
    return inspecionar.analisar_audio(arq, log, info, narracao)


def test_audio_limpo_nao_acusa_nada(tmp_path):
    r = _analisar(_audio(tmp_path, "limpo.wav", "sine=f=440:r=48000:d=6,volume=0.3"))
    assert r["picos_cortados"]["trechos"] == 0 and r["silencios"] == [] and r["saltos_volume"] == []


def test_audio_acha_clipping(tmp_path):
    r = _analisar(_audio(tmp_path, "alto.wav", "sine=f=440:r=48000:d=3,volume=16"))
    assert r["picos_cortados"]["trechos"] > 100 and r["picos_cortados"]["segundos"][0] < 0.1


def test_audio_acha_buraco_de_silencio(tmp_path):
    arq = _audio(tmp_path, "buraco.wav", "sine=f=440:r=48000:d=6,volume='if(between(t,2,3.5),0,0.3)':eval=frame")
    [s] = _analisar(arq)["silencios"]
    assert 1.9 <= s["inicio_s"] <= 2.1 and 1.3 <= s["dur_s"] <= 1.6


def test_audio_acha_salto_de_volume(tmp_path):
    arq = _audio(tmp_path, "salto.wav", "sine=f=440:r=48000:d=10,volume='if(lt(t,5),0.03,0.8)':eval=frame")
    [s] = _analisar(arq)["saltos_volume"]
    assert 5 <= s["segundo"] <= 7 and s["para_lufs"] - s["de_lufs"] >= 6


def test_audio_acha_voz_abafada_pela_musica(tmp_path):
    # sine sai com amplitude 1/8; "voz": tom de 1 kHz em sílabas de 125 ms; "música": ruído rosa contínuo quase tão alto quanto ela
    fala = "sine=f=1000:r=16000:d=8,volume='if(lt(mod(t,0.25),0.125),0.5,0)':eval=frame"
    assert inspecionar.voz_abafada(_audio(tmp_path, "fala.wav", fala)) == []
    misturado = _audio(tmp_path, "abafada.wav", f"{fala}[v];anoisesrc=color=pink:r=16000:amplitude=0.6:d=8[m];"
                                                "[v][m]amix=inputs=2:normalize=0")
    trechos = inspecionar.voz_abafada(misturado)
    assert trechos and trechos[0]["inicio_s"] == 0 and trechos[-1]["fim_s"] == 8
