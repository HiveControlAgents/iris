"""Testes do inspetor com um vídeo sintético gerado pelo próprio ffmpeg (sem baixar nada)."""
import json
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
    assert r["divergencias"] == []
    r = inspecionar.comparar_narracao("o olho acompanha", "o olho companha")
    assert r["divergencias"] == [{"roteiro": "acompanha", "ouvido": "companha"}]


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
