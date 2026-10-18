"""Inspeção de um vídeo gerado por IA: mede o que dá para medir e monta folhas de contato para a revisão visual.

Uso:
    python inspecionar.py video.mp4 [--roteiro roteiro.json] [--saida pasta] [--referencia-voz voz.wav]

Gera na pasta de saída (padrão: .iris/<nome-do-video>/):
    medidas.json   duração, resolução, loudness, cenas, cortes, congelamentos, telas pretas, narração
    folha_N.jpg    2 quadros por segundo, 6 por linha, com o tempo escrito em amarelo no canto

Só precisa de ffmpeg/ffprobe no PATH e Pillow. Opcionais: openai-whisper ou faster-whisper (compara o que foi
dito com o roteiro) e librosa (confere se a voz é a mesma da gravação de referência).
"""
from __future__ import annotations

import argparse
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
LIMIAR_CORTE = 0.3


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
            "tem_audio": any(s["codec_type"] == "audio" for s in dados["streams"])}


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


def comparar_narracao(roteiro_txt: str, ouvido_txt: str) -> dict:
    """Palavras do roteiro x o que foi ouvido: divergências costumam ser pronúncia errada ou palavra engolida."""
    a = [w for w in (_normalizar(p) for p in roteiro_txt.split()) if w]
    b = [w for w in (_normalizar(p) for p in ouvido_txt.split()) if w]
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    divergencias = [{"roteiro": " ".join(a[i1:i2]), "ouvido": " ".join(b[j1:j2])}
                    for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
    # números escritos por extenso no roteiro e em dígitos na transcrição não são erro de pronúncia
    divergencias = [d for d in divergencias if not re.search(r"\d", d["ouvido"])]
    return {"palavras_roteiro": len(a), "palavras_ouvidas": len(b), "taxa_acerto": round(sm.ratio(), 3),
            "divergencias": divergencias[:30]}


def transcrever(video: Path, idioma: str) -> str | None:
    """Transcrição com o Whisper que estiver instalado; sem nenhum, a comparação de narração é pulada."""
    try:
        from faster_whisper import WhisperModel
        modelo = WhisperModel("small", device="cpu", compute_type="int8")
        segmentos, _ = modelo.transcribe(str(video), language=idioma)
        return " ".join(s.text for s in segmentos)
    except ImportError:
        pass
    try:
        import whisper
        return whisper.load_model("small", device="cpu").transcribe(str(video), language=idioma, fp16=False)["text"]
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


def medir(video: Path, roteiro: dict | None, referencia_voz: Path | None, idioma: str) -> dict:
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
        filtros += ["-af", "ebur128=peak=true"]
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
        "folha": {"quadros_por_segundo": QPS, "colunas": COLUNAS, "segundos_por_imagem": SEG_POR_FOLHA},
    }
    roteiro_txt = " ".join(c.get("narracao", "") for c in (roteiro or {}).get("cenas", [])).strip()
    if roteiro_txt and info["tem_audio"]:
        ouvido = transcrever(video, idioma)
        medidas["narracao"] = (comparar_narracao(roteiro_txt, ouvido) if ouvido is not None
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
    """2 quadros por segundo, grandes o bastante para ver objetos sumindo, com o tempo exato no canto."""
    from PIL import Image, ImageDraw
    linhas = round(SEG_POR_FOLHA * QPS / COLUNAS)
    fonte, folhas = _fonte(22), []
    with tempfile.TemporaryDirectory() as tmp:
        _ffmpeg(["-y", "-i", str(video), "-vf", f"fps={QPS},scale={LARGURA_QUADRO}:-2", "-q:v", "4",
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
                t = (k * por_folha + i) / QPS          # o filtro fps=2 começa no quadro de t=0
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

    medidas = medir(a.video, roteiro, a.referencia_voz, a.idioma)
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
