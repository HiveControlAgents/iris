"""Inspeção de um vídeo gerado por IA: mede o que dá para medir e monta folhas de contato para a revisão visual.

Uso:
    python inspecionar.py video.mp4 [--roteiro roteiro.json] [--saida pasta] [--referencia-voz voz.wav]

Gera na pasta de saída (padrão: .iris/<nome-do-video>/):
    medidas.json   duração, resolução, loudness, cenas, cortes, congelamentos, telas pretas, narração
    folha_N.jpg    2 quadros por segundo, 6 por linha, com o tempo escrito em amarelo no canto

O áudio é analisado de verdade, além da transcrição: picos cortados (clipping), buracos de silêncio, saltos de
volume e trechos em que a música abafa a voz.

Só precisa de ffmpeg/ffprobe no PATH e Pillow. Opcionais: openai-whisper ou faster-whisper (compara o que foi
dito com o roteiro) e librosa (confere se a voz é a mesma da gravação de referência).
"""
from __future__ import annotations

import argparse
import array
import datetime as dt
import difflib
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

QPS, COLUNAS, SEG_POR_FOLHA, LARGURA_QUADRO = 2, 6, 12, 250   # 6x4 quadros = 12 s por imagem
# vídeo longo (mais de LONGO_S): 1 quadro a cada 5 s e 2 min por folha; a 2 qps um vídeo de 10 min daria 50 folhas
QPS_LONGO, SEG_POR_FOLHA_LONGO, LONGO_S = 0.2, 120, 180


def ritmo_folha(total: float) -> tuple[float, int]:
    """(quadros por segundo, segundos por folha) para a duração do vídeo."""
    return (QPS, SEG_POR_FOLHA) if total <= LONGO_S else (QPS_LONGO, SEG_POR_FOLHA_LONGO)
LIMIAR_CORTE = 0.3
SILENCIO_DB, SILENCIO_S = -45, 0.7    # buraco de silêncio: abaixo de -45 dBFS por 0,7 s ou mais
SALTO_LU = 6                          # salto de volume: loudness de curto prazo (3 s) muda 6 LU ou mais em 1 s
MODULACAO_DB = 10                     # voz abafada: na faixa da voz, as sílabas ficam a menos de 10 dB dos vãos


def _rodar(args: list[str]) -> str:
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stderr + r.stdout


def _ffmpeg(args: list[str]) -> str:
    return _rodar(["ffmpeg", "-hide_banner", "-nostdin", *args])


def info_video(video: Path) -> dict:
    saida = _rodar(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", str(video)])
    dados = json.loads(saida[saida.find("{"):])
    v = next((s for s in dados["streams"] if s["codec_type"] == "video"), {})
    num, _, den = (v.get("avg_frame_rate") or "0/1").partition("/")
    return {"duracao_s": round(float(dados["format"]["duration"]), 2),
            "tamanho_mb": round(video.stat().st_size / 2**20, 1),
            "largura": v.get("width"), "altura": v.get("height"),
            "fps": round(float(num) / float(den or 1), 2) if float(den or 1) else None,
            "tem_audio": any(s["codec_type"] == "audio" for s in dados["streams"]),
            "audio_hz": int(next((s.get("sample_rate", 0) for s in dados["streams"] if s["codec_type"] == "audio"), 0)),
            "audio_canais": next((s.get("channels", 1) for s in dados["streams"] if s["codec_type"] == "audio"), 0)}


def _metadados(video: Path, filtro: str) -> list[dict]:
    """Roda um filtro com metadata=print e devolve [{t, chave: valor}] por quadro."""
    with tempfile.TemporaryDirectory() as tmp:
        arq = Path(tmp) / "meta.txt"
        # o caminho vai relativo ao cwd do ffmpeg para não brigar com ':' e '\' do Windows dentro do filtro
        subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", "-i", str(video.resolve()), "-vf",
                        f"{filtro},metadata=print:file=meta.txt", "-an", "-f", "null", "-"],
                       capture_output=True, cwd=tmp)
        quadros = []
        if not arq.exists():
            return quadros
        for linha in arq.read_text(encoding="utf-8", errors="replace").splitlines():
            if linha.startswith("frame:"):
                m = re.search(r"pts_time:([\d.]+)", linha)
                quadros.append({"t": float(m.group(1)) if m else 0.0})
            elif "=" in linha and quadros:
                chave, valor = linha.split("=", 1)
                try:
                    quadros[-1][chave.split(".")[-1]] = float(valor)
                except ValueError:
                    pass
        return quadros


def _normalizar(palavra: str) -> str:
    p = unicodedata.normalize("NFKD", palavra.lower()).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", p)


PROB_MINIMA = 0.6      # palavra que o transcritor ouviu com menos certeza que isto entra em "duvidosas"
PARECIDA = 0.8         # semelhança mínima entre duas palavras para a troca ser só "suspeita", não erro


def comparar_narracao(roteiro_txt: str, ouvido_txt: str, duvidosas: list[str] | tuple = ()) -> dict:
    """Palavras do roteiro x o que foi ouvido. O transcritor (Whisper) corrige sozinho muita pronúncia torta, então
    uma taxa alta não prova que a voz falou certo. "erros": palavra inventada pela voz, engolida ou trocada;
    "suspeitas": o que tanto pode ser jeito do transcritor quanto pronúncia torta: palavra parecida ("alisios"/
    "aliseos"), palavras emendadas ("ar poderosas"/"arpoderosas") ou palavrinha de até 2 letras engolida ("viaja a
    centenas" sem o "a", elisão natural); "duvidosas": palavras ouvidas com pouca certeza. Número em dígitos ("200"
    por "duzentos") não conta."""
    a = [w for w in (_normalizar(p) for p in roteiro_txt.split()) if w]
    b = [w for w in (_normalizar(p) for p in ouvido_txt.split()) if w]
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    erros, suspeitas = [], []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal" or re.search(r"\d", " ".join(b[j1:j2])):
            continue
        item = {"roteiro": " ".join(a[i1:i2]), "ouvido": " ".join(b[j1:j2])}
        emendado = i2 > i1 and j2 > j1 and difflib.SequenceMatcher(None, "".join(a[i1:i2]), "".join(b[j1:j2])).ratio() >= PARECIDA
        engolida_curta = j2 == j1 and all(len(p) <= 2 for p in a[i1:i2])
        if emendado or engolida_curta:
            suspeitas.append(item)
        else:
            erros.append(item)
    return {"palavras_roteiro": len(a), "palavras_ouvidas": len(b), "taxa_acerto": round(sm.ratio(), 3),
            "erros": erros[:30], "suspeitas": suspeitas[:30], "duvidosas": list(duvidosas)[:30],
            "divergencias": (erros + suspeitas)[:30]}


def transcrever(video: Path, idioma: str) -> tuple[str, list[str]] | None:
    """Transcrição com o Whisper que estiver instalado: (texto, palavras ouvidas com pouca certeza). Sem nenhum
    Whisper, devolve None e a comparação de narração é pulada."""
    try:
        from faster_whisper import WhisperModel
        modelo = WhisperModel("small", device="cpu", compute_type="int8")
        segmentos = list(modelo.transcribe(str(video), language=idioma, word_timestamps=True)[0])
        return (" ".join(s.text for s in segmentos),
                [w.word.strip() for s in segmentos for w in (s.words or []) if w.probability < PROB_MINIMA])
    except ImportError:
        pass
    try:
        import whisper
        res = whisper.load_model("small", device="cpu").transcribe(str(video), language=idioma, fp16=False,
                                                                    word_timestamps=True)
        return (res["text"], [w["word"].strip() for s in res["segments"] for w in s.get("words", [])
                              if w.get("probability", 1.0) < PROB_MINIMA])
    except ImportError:
        return None


def _perfil_voz(arquivo):
    import librosa
    import numpy as np
    y, sr = librosa.load(str(arquivo), sr=16000)
    f0 = librosa.pyin(y, fmin=60, fmax=300, sr=sr)[0]
    f0 = f0[~np.isnan(f0)]
    meio = len(f0) // 2
    return {"f0": float(np.median(f0)), "deriva": float(np.median(f0[meio:]) - np.median(f0[:meio])),
            "mfcc": librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)[1:].mean(axis=1)}


def medir_voz(video: Path, referencia: Path) -> dict:
    """A voz do vídeo é a voz aprovada? Compara timbre (MFCC médio, cosseno) e tom com a gravação de referência.
    Calibração: uma voz clonada da referência deu 0,98; uma voz parecida, mas reprovada de ouvido, deu 0,86."""
    try:
        import numpy as np
        with tempfile.TemporaryDirectory() as tmp:
            wav = Path(tmp) / "voz.wav"
            _ffmpeg(["-y", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", str(wav)])
            n, r = _perfil_voz(wav), _perfil_voz(referencia)
    except Exception as e:                         # a medida da voz nunca derruba a inspeção
        return {"erro": str(e)[:200]}
    sim = float(np.dot(n["mfcc"], r["mfcc"]) / np.linalg.norm(n["mfcc"]) / np.linalg.norm(r["mfcc"]))
    return {"semelhanca_timbre": round(sim, 3), "tom_medio_hz": round(n["f0"]), "tom_referencia_hz": round(r["f0"]),
            "deriva_hz": round(n["deriva"]), "confere": sim >= 0.95 and abs(n["f0"] - r["f0"]) <= 15,
            "como_ler": "semelhança abaixo de 0,95 ou tom a mais de 15 Hz da referência = não é a mesma voz"}


def _pcm(video: Path, args: list[str]) -> array.array:
    """Amostras de 16 bits do áudio, depois dos filtros/opções de `args`."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", "-loglevel", "error", "-i", str(video), "-vn", *args,
                        "-f", "s16le", "-acodec", "pcm_s16le", "-"], capture_output=True)
    amostras = array.array("h")
    amostras.frombytes(r.stdout[:len(r.stdout) // 2 * 2])
    if sys.byteorder == "big":
        amostras.byteswap()
    return amostras


def _agrupar(tempos: list[float], folga: float) -> list[float]:
    """Junta marcas a menos de `folga` segundos da anterior (um defeito longo vira uma marca só)."""
    saida: list[float] = []
    ultimo = -1e9
    for t in tempos:
        if t - ultimo > folga:
            saida.append(round(t, 1))
        ultimo = t
    return saida


def picos_cortados(video: Path, hz: int, canais: int) -> dict:
    """Clipping: 3 ou mais amostras seguidas no teto digital, em qualquer canal (sem mixar, que esconderia o pico)."""
    a, canais, hz = _pcm(video, []), canais or 1, hz or 48000
    marcas = []
    for c in range(canais):
        seguidas = 0
        for i, x in enumerate(a[c::canais]):
            if x >= 32766 or x <= -32767:
                seguidas += 1
                if seguidas == 3:
                    marcas.append(i / hz)
            else:
                seguidas = 0
    return {"trechos": len(marcas), "segundos": _agrupar(sorted(marcas), 0.5)[:20]}


def voz_abafada(video: Path, de: float = 0.0, ate: float | None = None) -> list[dict]:
    """Música abafando a voz. A fala tem sílabas e vãos: na faixa da voz (300 a 3400 Hz) os quadros fortes ficam
    bem acima dos fracos. Quando a música preenche os vãos, essa modulação cai. Mede a cada 2 s, em quadros de 50 ms,
    a diferença entre o percentil 90 e o 10; abaixo de MODULACAO_DB com som presente (> -40 dBFS) é suspeito."""
    hz = 16000
    a = _pcm(video, ["-af", "highpass=f=300,lowpass=f=3400", "-ac", "1", "-ar", str(hz)])
    quadro = hz // 20
    db = []
    for i in range(0, len(a) - quadro + 1, quadro):
        energia = sum(x * x for x in a[i:i + quadro]) / quadro
        db.append(10 * math.log10(energia / 32768 ** 2) if energia else -120.0)
    trechos: list[dict] = []
    for k in range(0, len(db) - 39, 40):                     # 40 quadros de 50 ms = 2 s
        inicio = k / 20
        if inicio < de or (ate is not None and inicio + 2 > ate):
            continue
        janela = sorted(db[k:k + 40])
        p10, p90 = janela[4], janela[35]
        if p90 > -40 and p90 - p10 < MODULACAO_DB:
            if trechos and abs(trechos[-1]["fim_s"] - inicio) < 0.01:
                trechos[-1]["fim_s"] = inicio + 2
                trechos[-1]["modulacao_db"] = min(trechos[-1]["modulacao_db"], round(p90 - p10, 1))
            else:
                trechos.append({"inicio_s": inicio, "fim_s": inicio + 2, "modulacao_db": round(p90 - p10, 1)})
    return trechos


def analisar_audio(video: Path, log: str, info: dict, narracao: tuple[float, float] | None) -> dict:
    """Áudio além da transcrição. `log` é a saída do ffmpeg com ebur128 e silencedetect; `narracao` é o intervalo
    (início, fim) em que há fala, para não confundir introdução musical com voz abafada."""
    total = info["duracao_s"]
    silencios = [{"inicio_s": round(float(fim) - float(dur), 1), "dur_s": round(float(dur), 1)} for fim, dur in
                 re.findall(r"silence_end: ([\d.]+) \| silence_duration: ([\d.]+)", log)]
    # silêncio colado no começo ou no fim é respiro de edição, não buraco
    buracos = [s for s in silencios if s["inicio_s"] > 0.3 and s["inicio_s"] + s["dur_s"] < total - 0.3]
    curto = [(float(t), float(s)) for t, s in re.findall(r"t:\s*([\d.]+)\s+TARGET:.*?\sS:\s*(-?[\d.]+)", log)]
    saltos, ultimo = [], -9.0
    for (t0, s0), (t1, s1) in zip(curto, curto[10:]):         # 10 medidas de 0,1 s = 1 s
        if t1 > 3 and min(s0, s1) > -50 and abs(s1 - s0) >= SALTO_LU and t1 - ultimo > 1.5:
            saltos.append({"segundo": round(t1, 1), "de_lufs": s0, "para_lufs": s1})
            ultimo = t1
    de, ate = narracao or (0.0, None)
    return {"picos_cortados": picos_cortados(video, info.get("audio_hz", 0), info.get("audio_canais", 1)),
            "silencios": buracos, "saltos_volume": saltos[:20], "voz_abafada": voz_abafada(video, de, ate)[:20],
            "como_ler": "picos_cortados.trechos > 0 = distorção; silencios = buraco de 0,7 s ou mais no meio do "
                        "vídeo; saltos_volume = volume muda 6 LU ou mais em 1 s; voz_abafada = trecho em que a "
                        "música (ou ruído) preenche os vãos da fala (heurística: confirme pela transcrição)"}


def fronteiras(roteiro: dict | None, cortes: list[float], total: float) -> list[tuple[float, float, dict]]:
    """Início e fim de cada cena: do roteiro (inicio_s/fim_s ou dur_s), ou dos cortes bruscos quando não há roteiro."""
    cenas = (roteiro or {}).get("cenas") or []
    if cenas and all("inicio_s" in c and "fim_s" in c for c in cenas):
        return [(float(c["inicio_s"]), float(c["fim_s"]), c) for c in cenas]
    if cenas and all("dur_s" in c for c in cenas):
        saida, inicio = [], 0.0
        for c in cenas:
            saida.append((inicio, inicio + float(c["dur_s"]), c))
            inicio += float(c["dur_s"])
        return saida
    marcas = [0.0] + [t for t in cortes if 0.5 < t < total - 0.5] + [total]
    pares = [(a, b) for a, b in zip(marcas, marcas[1:]) if b - a >= 0.5]
    # com roteiro sem tempos, casa a narração com as cenas detectadas só quando a contagem bate
    if cenas and len(cenas) == len(pares):
        return [(a, b, c) for (a, b), c in zip(pares, cenas)]
    return [(a, b, {}) for a, b in pares]


def medir(video: Path, roteiro: dict | None, referencia_voz: Path | None, idioma: str, max_refazer: int = 3) -> dict:
    info = info_video(video)
    total = info["duracao_s"]

    # brilho (YAVG) e saturação (SATAVG) 4x por segundo; cortes bruscos (mudança de cena > LIMIAR_CORTE)
    stats = _metadados(video, "fps=4,scale=270:-2,signalstats")
    cortes = [round(q["t"], 2) for q in _metadados(video, f"scale=270:-2,select='gt(scene,{LIMIAR_CORTE})'")]

    cenas = []
    for n, (inicio, fim, c) in enumerate(fronteiras(roteiro, cortes, total), 1):
        dur = fim - inicio
        trecho = [q for q in stats if inicio <= q["t"] < fim]
        um_seg = max(1, len(trecho) // max(1, round(dur)))
        media = lambda qs, k: round(sum(q.get(k, 0) for q in qs) / len(qs), 1) if qs else None  # noqa: E731
        cena = {"n": n, "inicio_s": round(inicio, 2), "fim_s": round(fim, 2), "dur_s": round(dur, 2),
                "brilho_ini": media(trecho[:um_seg], "YAVG"), "brilho_fim": media(trecho[-um_seg:], "YAVG"),
                "saturacao_ini": media(trecho[:um_seg], "SATAVG"), "saturacao_fim": media(trecho[-um_seg:], "SATAVG"),
                # cortes dentro da cena (longe da fronteira) = salto, troca de assunto ou objeto que surge/some
                "cortes_internos_s": [t for t in cortes if inicio + 0.3 < t < fim - 0.3]}
        if c.get("narracao"):
            cena["narracao"] = c["narracao"]
            cena["palavras_por_s"] = round(len(c["narracao"].split()) / dur, 2) if dur else None
        for chave in ("prompt", "quadro", "prompt_video", "movimento"):
            if c.get(chave):
                cena[chave] = c[chave]
        cenas.append(cena)

    filtros = ["-i", str(video), "-vf", "freezedetect=n=0.002:d=2,blackdetect=d=0.3"]
    if info["tem_audio"]:
        filtros += ["-af", f"ebur128=peak=true,silencedetect=n={SILENCIO_DB}dB:d={SILENCIO_S}"]
    log = _ffmpeg([*filtros, "-f", "null", "-"])
    lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", log)
    pico = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", log)
    congelados = [{"inicio_s": round(float(a), 1), "dur_s": round(float(b), 1)} for a, b in
                  re.findall(r"freeze_start: ([\d.]+).*?freeze_duration: ([\d.]+)", log, re.S)]
    pretas = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", log)

    medidas = {
        "video_arquivo": video.name,
        "titulo": (roteiro or {}).get("titulo"), "tema": (roteiro or {}).get("tema"),
        "estilo_visual": (roteiro or {}).get("estilo_visual"),
        "inspecionado_em": dt.datetime.now().isoformat(timespec="seconds"),
        "video": info,
        "audio": {"lufs_integrado": float(lufs[-1]) if lufs else None,
                  "pico_dbfs": float(pico[-1]) if pico else None},
        "cenas": cenas,
        "cortes_bruscos_s": cortes,
        "congelamentos": congelados,
        "telas_pretas": [{"inicio_s": float(a), "fim_s": float(b)} for a, b in pretas],
        "max_refazer": max_refazer,
        "folha": dict(zip(("quadros_por_segundo", "segundos_por_imagem"), ritmo_folha(info["duracao_s"])),
                      colunas=COLUNAS),
    }
    if info["tem_audio"]:
        com_fala = [c for c in cenas if c.get("narracao")]
        trecho_fala = (com_fala[0]["inicio_s"], com_fala[-1]["fim_s"]) if com_fala else None
        medidas["audio"].update(analisar_audio(video, log, info, trecho_fala))
    roteiro_txt = " ".join(c.get("narracao", "") for c in (roteiro or {}).get("cenas", [])).strip()
    if roteiro_txt and info["tem_audio"]:
        ouvido = transcrever(video, idioma)
        medidas["narracao"] = (comparar_narracao(roteiro_txt, *ouvido) if ouvido is not None
                               else {"pulado": "instale faster-whisper ou openai-whisper para comparar a narração"})
    if referencia_voz and info["tem_audio"]:
        medidas["audio"]["identidade_voz"] = medir_voz(video, referencia_voz)
    return medidas


def _fonte(tamanho: int):
    from PIL import ImageFont
    for nome in ("DejaVuSans-Bold.ttf", "arialbd.ttf", "Arial Bold.ttf", "Arial.ttf"):
        try:
            return ImageFont.truetype(nome, tamanho)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=tamanho)
    except TypeError:                                    # Pillow antigo
        return ImageFont.load_default()


def folhas_de_contato(video: Path, total: float, saida: Path) -> list[Path]:
    """2 quadros por segundo (1 a cada 5 s em vídeo longo), grandes o bastante para ver objetos sumindo, com o
    tempo exato no canto."""
    from PIL import Image, ImageDraw
    qps, seg = ritmo_folha(total)
    linhas = round(seg * qps / COLUNAS)
    fonte, folhas = _fonte(22), []
    with tempfile.TemporaryDirectory() as tmp:
        _ffmpeg(["-y", "-i", str(video), "-vf", f"fps={qps},scale={LARGURA_QUADRO}:-2", "-q:v", "4",
                 str(Path(tmp) / "q_%05d.jpg")])
        quadros = sorted(Path(tmp).glob("q_*.jpg"))
        por_folha = COLUNAS * linhas
        for k in range(math.ceil(len(quadros) / por_folha) if quadros else 0):
            lote = quadros[k * por_folha:(k + 1) * por_folha]
            with Image.open(lote[0]) as primeira:          # fechar já: no Windows arquivo aberto trava a limpeza do tmp
                (w, h), pad = primeira.size, 4
            folha = Image.new("RGB", (COLUNAS * (w + pad) + pad, linhas * (h + pad) + pad), "black")
            for i, arq in enumerate(lote):
                with Image.open(arq) as im:
                    q = im.convert("RGB")
                d = ImageDraw.Draw(q)
                t = (k * por_folha + i) / qps          # o filtro fps começa no quadro de t=0
                texto = f"{int(t // 60)}:{t % 60:04.1f}"
                caixa = d.textbbox((8, 8), texto, font=fonte)
                d.rectangle((caixa[0] - 4, caixa[1] - 4, caixa[2] + 4, caixa[3] + 4), fill=(0, 0, 0))
                d.text((8, 8), texto, fill=(255, 220, 0), font=fonte)
                folha.paste(q, (pad + (i % COLUNAS) * (w + pad), pad + (i // COLUNAS) * (h + pad)))
            destino = saida / f"folha_{k + 1}.jpg"
            folha.save(destino, quality=80)
            folhas.append(destino)
    return folhas


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Mede um vídeo gerado por IA e monta folhas de contato para revisão.")
    ap.add_argument("video", type=Path)
    ap.add_argument("--roteiro", type=Path, help="JSON com 'cenas' (narracao, e inicio_s/fim_s ou dur_s opcionais)")
    ap.add_argument("--saida", type=Path, help="pasta de saída (padrão: .iris/<nome-do-video>)")
    ap.add_argument("--referencia-voz", type=Path, help="gravação da voz aprovada, para conferir o timbre (librosa)")
    ap.add_argument("--idioma", default="pt", help="idioma da narração para o Whisper (padrão: pt)")
    ap.add_argument("--max-refazer", type=int, default=3, help="máximo de cenas que a revisão pode mandar refazer")
    a = ap.parse_args(argv)

    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        print("ERRO: ffmpeg e ffprobe precisam estar no PATH.", file=sys.stderr)
        return 2
    if not a.video.exists():
        print(f"ERRO: vídeo não encontrado: {a.video}", file=sys.stderr)
        return 2
    roteiro = json.loads(a.roteiro.read_text(encoding="utf-8")) if a.roteiro else None
    saida = a.saida or Path(".iris") / a.video.stem
    saida.mkdir(parents=True, exist_ok=True)

    medidas = medir(a.video, roteiro, a.referencia_voz, a.idioma, a.max_refazer)
    folhas = folhas_de_contato(a.video, medidas["video"]["duracao_s"], saida)
    medidas["folhas"] = [f.name for f in folhas]
    (saida / "medidas.json").write_text(json.dumps(medidas, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"medidas: {saida / 'medidas.json'}")
    for f in folhas:
        print(f"folha:   {f}")
    print(f"cenas: {len(medidas['cenas'])} | cortes bruscos: {len(medidas['cortes_bruscos_s'])} | "
          f"congelamentos: {len(medidas['congelamentos'])} | LUFS: {medidas['audio']['lufs_integrado']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
