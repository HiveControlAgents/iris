"""Benchmark público da ÍRIS: roda a inspeção + revisão sobre vários vídeos e mede contra rótulos humanos.

    python benchmark/bench.py adicionar video.mp4 --id meu-video [--roteiro roteiro.json] [--fonte nosso|terceiro]
                                       [--licenca "..."] [--link URL] [--titulo "..."]
    python benchmark/bench.py pasta PASTA [--padrao "*/video.mp4"] [--roteiro-ao-lado roteiro.json] [--limite N]
    python benchmark/bench.py tabela       # refaz a tabela de defeitos no benchmark/README.md
    python benchmark/bench.py metricas     # precisão e revocação a partir de benchmark/rotulos/*.md

`adicionar` revisa um vídeo numa pasta de trabalho só dele (sem histórico de outros vídeos, para cada revisão ser
independente), copia medidas.json, revisao.json e revisao.md para benchmark/resultados/<id>/, cria o arquivo de
rótulos e atualiza a tabela. `pasta` faz isso para todo vídeo de uma pasta que ainda não está no benchmark: é o
gancho para o vídeo de toda noite entrar sozinho. Os vídeos não entram no repositório, só as revisões; vídeo de
terceiros (Veo, Kling, Sora...) entra com `--fonte terceiro --link URL`.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
RESULTADOS, ROTULOS, TRABALHO = AQUI / "resultados", AQUI / "rotulos", AQUI / "trabalho"
VIDEOS, LEIAME, DEFEITOS = AQUI / "videos.json", AQUI / "README.md", AQUI / "defeitos.csv"
TIPOS = ["visual", "narracao", "ritmo", "audio", "legenda", "tecnico"]
CAMINHO_LOCAL = re.compile(r"(?:(?<![A-Za-z])[A-Za-z]:[\\/]|\\\\|/(?:home|Users|mnt|tmp)/)[^\s\"'`)\]|]*")
MARCA_ROTULO = re.compile(r"^- \[([ xX])\] certo\s+\[([ xX])\] errado \| (.*)$")


def slug(texto: str, limite: int = 48) -> str:
    t = unicodedata.normalize("NFKD", texto.lower()).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:limite].strip("-")


def limpar_caminhos(texto: str) -> str:
    """Tira caminhos do disco (C:\\..., /home/...) antes de qualquer coisa ir para o repositório."""
    return CAMINHO_LOCAL.sub("<local>", texto)


def _ler(arq: Path, padrao):
    return json.loads(arq.read_text(encoding="utf-8")) if arq.exists() else padrao


def _tempo(s) -> str:
    return f"{int(s // 60)}:{s % 60:04.1f}" if isinstance(s, (int, float)) else "?"


def adicionar(video: Path, ident: str, roteiro: Path | None = None, fonte: str = "nosso", licenca: str = "",
              link: str = "", titulo: str = "", referencia_voz: Path | None = None) -> bool:
    trabalho = TRABALHO / ident
    shutil.rmtree(trabalho, ignore_errors=True)
    trabalho.mkdir(parents=True)
    cmd = [sys.executable, "-m", "iris", str(video.resolve())]
    if roteiro:
        cmd += ["--roteiro", str(roteiro.resolve())]
    if referencia_voz:
        cmd += ["--referencia-voz", str(referencia_voz.resolve())]
    env = {**os.environ, "PYTHONPATH": str(RAIZ) + os.pathsep + os.environ.get("PYTHONPATH", "")}
    subprocess.run(cmd, cwd=trabalho, env=env)
    pasta = trabalho / ".iris" / video.stem
    if not (pasta / "revisao.json").exists():
        print(f"ERRO: sem revisão para {ident} (o Claude Code está no PATH?)", file=sys.stderr)
        return False
    destino = RESULTADOS / ident
    destino.mkdir(parents=True, exist_ok=True)
    for nome in ("medidas.json", "revisao.json", "revisao.md"):
        (destino / nome).write_text(limpar_caminhos((pasta / nome).read_text(encoding="utf-8")), encoding="utf-8")
    medidas = _ler(destino / "medidas.json", {})
    titulo = titulo or medidas.get("titulo") or ident
    videos = [v for v in _ler(VIDEOS, []) if v["id"] != ident]
    videos.append({"id": ident, "titulo": titulo, "fonte": fonte, "licenca": licenca, "link": link,
                   "duracao_s": medidas.get("video", {}).get("duracao_s"), "adicionado_em": dt.date.today().isoformat()})
    VIDEOS.write_text(json.dumps(sorted(videos, key=lambda v: v["id"]), ensure_ascii=False, indent=1) + "\n",
                      encoding="utf-8")
    criar_rotulos(ident, titulo, link)
    tabela()
    print(f"benchmark: {ident} adicionado")
    return True


def criar_rotulos(ident: str, titulo: str, link: str = "") -> Path:
    """Checklist para um humano marcar cada achado da ÍRIS como certo ou errado e listar o que ela não viu."""
    arq = ROTULOS / f"{ident}.md"
    if arq.exists():                                      # nunca apaga rótulos já preenchidos
        return arq
    ROTULOS.mkdir(exist_ok=True)
    revisao = _ler(RESULTADOS / ident / "revisao.json", {})
    linhas = [f"# Rótulos: {titulo}", "", f"Vídeo: {link or 'arquivo local (não está no repositório)'} · id `{ident}`",
              "", "Assista ao vídeo e marque com `x` / Watch the video and mark with `x`.", "",
              "## Achados da ÍRIS / ÍRIS findings", ""]
    for p in revisao.get("problemas", []):
        desc = " ".join(str(p.get("descricao", "")).split()).replace("|", "/")
        linhas.append(f"- [ ] certo  [ ] errado | {_tempo(p.get('segundo'))} | {p.get('tipo', '')} | "
                      f"{p.get('gravidade', '')} | {desc}")
    linhas += ["", "## Defeitos que a ÍRIS não viu / Missed defects", "",
               "Um por linha / one per line: `- segundo | tipo | descrição`", "",
               "<!-- exemplo: - 0:12 | visual | mão com seis dedos -->", ""]
    arq.write_text("\n".join(linhas), encoding="utf-8")
    return arq


def ler_rotulos(arq: Path) -> dict:
    """{'certos', 'errados', 'pendentes', 'perdidos'} de um arquivo de rótulos."""
    r = {"certos": 0, "errados": 0, "pendentes": 0, "perdidos": 0}
    secao = ""
    for linha in arq.read_text(encoding="utf-8").splitlines():
        if linha.startswith("## "):
            secao = "perdidos" if "não viu" in linha or "Missed" in linha else "achados"
            continue
        m = MARCA_ROTULO.match(linha.strip())
        if m:
            certo, errado = m.group(1) != " ", m.group(2) != " "
            r["certos" if certo and not errado else "errados" if errado and not certo else "pendentes"] += 1
        elif secao == "perdidos" and linha.startswith("- "):
            r["perdidos"] += 1
    return r


def _trocar_secao(texto: str, nome: str, conteudo: str) -> str:
    ini, fim = f"<!-- {nome}:inicio -->", f"<!-- {nome}:fim -->"
    if ini not in texto:
        return texto.rstrip() + f"\n\n{ini}\n{conteudo}\n{fim}\n"
    return texto[:texto.index(ini) + len(ini)] + "\n" + conteudo + "\n" + texto[texto.index(fim):]


def tabela() -> str:
    """Tabela de defeitos por vídeo e por tipo (com os segundos) no README do benchmark, e defeitos.csv."""
    videos = _ler(VIDEOS, [])
    linhas = ["| vídeo | nota | defeitos | " + " | ".join(TIPOS) + " | onde (segundo e tipo) |",
              "|---|---|---|" + "---|" * len(TIPOS) + "---|"]
    csv = ["id,segundo,tipo,gravidade,descricao"]
    for v in videos:
        r = _ler(RESULTADOS / v["id"] / "revisao.json", {})
        probs = r.get("problemas", [])
        por_tipo = [sum(1 for p in probs if p.get("tipo") == t) for t in TIPOS]
        onde = "; ".join(f"{_tempo(p.get('segundo'))} {p.get('tipo', '')}" for p in probs)
        nome = f"[{v['titulo'][:50]}]({v['link']})" if v.get("link") else v["titulo"][:50]
        linhas.append(f"| {nome} | {r.get('nota', '?')} | {len(probs)} | " + " | ".join(map(str, por_tipo)) +
                      f" | {onde} |")
        for p in probs:
            desc = " ".join(str(p.get("descricao", "")).split()).replace('"', "'")
            csv.append(f'{v["id"]},{p.get("segundo", "")},{p.get("tipo", "")},{p.get("gravidade", "")},"{desc}"')
    conteudo = "\n".join(linhas)
    LEIAME.write_text(_trocar_secao(LEIAME.read_text(encoding="utf-8") if LEIAME.exists() else "", "tabela",
                                    conteudo), encoding="utf-8")
    DEFEITOS.write_text("\n".join(csv) + "\n", encoding="utf-8")
    return conteudo


def metricas() -> dict:
    """Precisão = achados certos / achados julgados; revocação = certos / (certos + defeitos que ela não viu).
    Só entram vídeos com todos os achados marcados."""
    total = {"certos": 0, "errados": 0, "perdidos": 0, "videos": 0, "pendentes": 0}
    por_tipo: dict[str, list[int]] = {}                   # tipo -> [certos, errados]
    for arq in sorted(ROTULOS.glob("*.md")):
        r = ler_rotulos(arq)
        if r["pendentes"] or not (r["certos"] or r["errados"] or r["perdidos"]):
            total["pendentes"] += 1
            continue
        total["videos"] += 1
        for k in ("certos", "errados", "perdidos"):
            total[k] += r[k]
        for linha in arq.read_text(encoding="utf-8").splitlines():
            m = MARCA_ROTULO.match(linha.strip())
            if m:
                tipo = (m.group(3).split("|") + ["", ""])[1].strip() or "?"
                por_tipo.setdefault(tipo, [0, 0])[0 if m.group(1) != " " else 1] += 1
    julgados = total["certos"] + total["errados"]
    total["precisao"] = round(total["certos"] / julgados, 3) if julgados else None
    total["revocacao"] = (round(total["certos"] / (total["certos"] + total["perdidos"]), 3)
                          if total["certos"] + total["perdidos"] else None)
    total["precisao_por_tipo"] = {t: round(c / (c + e), 3) for t, (c, e) in sorted(por_tipo.items())}
    pct = lambda x: f"{x:.0%}" if x is not None else "—"  # noqa: E731
    tipos = "".join(f"| {t} | {pct(total['precisao_por_tipo'][t])} | {c} | {e} |\n"
                    for t, (c, e) in sorted(por_tipo.items()))
    conteudo = (f"| rotulados / labeled | precisão / precision | revocação / recall | certos | errados | perdidos |\n"
                f"|---|---|---|---|---|---|\n"
                f"| {total['videos']} (pendentes: {total['pendentes']}) | {pct(total['precisao'])} | "
                f"{pct(total['revocacao'])} | {total['certos']} | {total['errados']} | {total['perdidos']} |\n\n"
                + (f"| tipo / type | precisão / precision | certos | errados |\n|---|---|---|---|\n{tipos}\n"
                   if tipos else "") +
                f"_Atualizado em {dt.date.today().isoformat()} com `python benchmark/bench.py metricas`._")
    LEIAME.write_text(_trocar_secao(LEIAME.read_text(encoding="utf-8") if LEIAME.exists() else "", "metricas",
                                    conteudo), encoding="utf-8")
    return total


def id_do_video(video: Path) -> str:
    """Id de um vídeo achado numa pasta: o nome da pasta dele (ou pasta-arquivo, se não se chamar video.mp4)."""
    return slug(video.parent.name if video.stem == "video" else f"{video.parent.name}-{video.stem}")


def pasta(raiz: Path, padrao: str, roteiro_ao_lado: str, limite: int, fonte: str, licenca: str) -> int:
    """Adiciona todo vídeo de `raiz` que ainda não está no benchmark (o gancho do vídeo de toda noite)."""
    feitos = {v["id"] for v in _ler(VIDEOS, [])}
    novos = 0
    for video in sorted(raiz.glob(padrao)):
        ident = id_do_video(video)
        if ident in feitos:
            continue
        if novos >= limite:
            break
        roteiro = video.parent / roteiro_ao_lado if roteiro_ao_lado else None
        if adicionar(video, ident, roteiro if roteiro and roteiro.exists() else None, fonte, licenca):
            novos += 1
    print(f"benchmark: {novos} vídeo(s) novo(s)")
    return novos


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="bench.py", description="Benchmark público da ÍRIS.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a1 = sub.add_parser("adicionar", help="revisa um vídeo e põe no benchmark")
    a1.add_argument("video", type=Path)
    a1.add_argument("--id", required=True)
    a1.add_argument("--roteiro", type=Path)
    a1.add_argument("--referencia-voz", type=Path)
    a1.add_argument("--fonte", choices=["nosso", "terceiro"], default="nosso")
    a1.add_argument("--licenca", default="")
    a1.add_argument("--link", default="")
    a1.add_argument("--titulo", default="")
    a2 = sub.add_parser("pasta", help="adiciona os vídeos de uma pasta que ainda não estão no benchmark")
    a2.add_argument("raiz", type=Path)
    a2.add_argument("--padrao", default="*/video.mp4")
    a2.add_argument("--roteiro-ao-lado", default="roteiro.json", help="nome do roteiro na pasta de cada vídeo")
    a2.add_argument("--limite", type=int, default=50, help="máximo de vídeos por rodada")
    a2.add_argument("--fonte", choices=["nosso", "terceiro"], default="nosso")
    a2.add_argument("--licenca", default="")
    sub.add_parser("tabela")
    sub.add_parser("metricas")
    a = ap.parse_args(argv)
    if a.cmd == "adicionar":
        return 0 if adicionar(a.video, slug(a.id), a.roteiro, a.fonte, a.licenca, a.link, a.titulo,
                              a.referencia_voz) else 1
    if a.cmd == "pasta":
        pasta(a.raiz, a.padrao, a.roteiro_ao_lado, a.limite, a.fonte, a.licenca)
    elif a.cmd == "tabela":
        print(tabela())
    else:
        print(json.dumps(metricas(), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
