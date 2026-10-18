"""ÍRIS na linha de comando: inspeciona um ou mais vídeos e, se o Claude Code estiver instalado, escreve a revisão.

    python -m iris video.mp4 [outro.mp4 ...] [--roteiro roteiro.json] [--sem-revisao] [--resumo resumo.md]
    iris video.mp4        (depois de `pipx install git+https://github.com/HiveControlAgents/iris`)

Para cada vídeo grava em .iris/<nome-do-video>/ as medidas e as folhas de contato e, com o Claude Code no PATH,
revisao.json e revisao.md. --resumo junta tudo num Markdown (é o que a GitHub Action posta no PR).
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path


def pasta_skill() -> Path:
    try:
        import iris.skill                                # instalado com pip/pipx
        return Path(list(iris.skill.__path__)[0])
    except ImportError:                                  # rodando de dentro do repositório
        return Path(__file__).resolve().parents[1] / "skills" / "revisar-video"


SKILL = pasta_skill()
sys.path.insert(0, str(SKILL / "scripts"))
import inspecionar  # noqa: E402

PEDIDO = """Revise o vídeo {video} seguindo a skill abaixo. A inspeção (passo 1) já foi feita: medidas.json e as folhas
de contato estão em {pasta}. Faça os passos 2 a 5, com os critérios de {criterios}, e grave revisao.json e revisao.md
nessa pasta. Nunca escreva caminhos absolutos do disco na revisão.{lingua}

{skill}"""


def revisar(video: Path, pasta: Path, revisao_em: str | None = None) -> bool:
    """Revisão pelo Claude Code em modo não interativo (`claude -p`). Sem o Claude Code no PATH, devolve False."""
    claude = shutil.which("claude")
    if not claude:
        return False
    lingua = f" Escreva revisao.md e os textos de revisao.json na língua '{revisao_em}'." if revisao_em else ""
    pedido = PEDIDO.format(video=video, pasta=pasta.resolve(), criterios=SKILL / "criterios.md", lingua=lingua,
                           skill=(SKILL / "SKILL.md").read_text(encoding="utf-8"))
    inicio = time.time()
    with open(pasta / "claude.log", "w", encoding="utf-8") as log:      # a conversa do Claude fica fora da tela
        subprocess.run([claude, "-p", "--permission-mode", "acceptEdits", "--add-dir", str(SKILL),
                        "--allowedTools", "Read,Write,Edit,Glob"], input=pedido, text=True, encoding="utf-8",
                       stdout=log, stderr=subprocess.STDOUT)
    feita = pasta / "revisao.json"
    return feita.exists() and feita.stat().st_mtime >= inicio


def _tempo(s) -> str:
    return f"{int(s // 60)}:{s % 60:04.1f}" if isinstance(s, (int, float)) else "?"


def resumo(pasta: Path) -> str:
    """Markdown curto de um vídeo: nota e problemas da revisão, se houver, e as medidas que já acusam defeito."""
    m = json.loads((pasta / "medidas.json").read_text(encoding="utf-8"))
    v, a = m["video"], m["audio"]
    linhas = [f"### {m['video_arquivo']}", ""]
    arq = pasta / "revisao.json"
    r = json.loads(arq.read_text(encoding="utf-8")) if arq.exists() else None
    if r:
        linhas += [f"**Nota {r.get('nota')}**: {r.get('resumo', '')}", ""]
    linhas.append(f"{v['duracao_s']} s · {v['largura']}x{v['altura']} · LUFS {a.get('lufs_integrado')} · "
                  f"pico {a.get('pico_dbfs')} dBFS · {len(m['cenas'])} cenas · {len(m['cortes_bruscos_s'])} cortes")
    alertas = [f"congelada {_tempo(c['inicio_s'])} ({c['dur_s']} s)" for c in m["congelamentos"]]
    alertas += [f"tela preta {_tempo(p['inicio_s'])}" for p in m["telas_pretas"]]
    alertas += [f"narração: '{e['roteiro']}' virou '{e['ouvido']}'" for e in (m.get("narracao") or {}).get("erros", [])]
    if alertas:
        linhas += ["", "Medidas: " + "; ".join(alertas)]
    if r and r.get("problemas"):
        linhas += ["", "| segundo | tipo | gravidade | problema |", "|---|---|---|---|"]
        linhas += [f"| {_tempo(p.get('segundo'))} | {p.get('tipo', '')} | {p.get('gravidade', '')} | "
                   f"{str(p.get('descricao', '')).replace('|', '/')} |" for p in r["problemas"]]
    if r and r.get("refazer"):
        linhas += ["", "Refazer: " + "; ".join(f"cena {c.get('cena')} ({c.get('motivo', '')})" for c in r["refazer"])]
    if not r:
        linhas += ["", "_Só as medidas automáticas: sem Claude Code, a revisão visual não foi feita._"]
    return "\n".join(linhas) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="iris", description="Inspeciona e revisa vídeos gerados por IA.")
    ap.add_argument("videos", type=Path, nargs="+")
    ap.add_argument("--roteiro", type=Path, help="JSON com 'cenas' (só com um vídeo)")
    ap.add_argument("--referencia-voz", type=Path, help="gravação da voz aprovada (librosa)")
    ap.add_argument("--idioma", default="pt", help="idioma da narração para o Whisper (padrão: pt)")
    ap.add_argument("--sem-revisao", action="store_true", help="só a inspeção, sem chamar o Claude Code")
    ap.add_argument("--revisao-em", help="língua da revisão, por exemplo en (padrão: a da skill, português)")
    ap.add_argument("--resumo", type=Path, help="grava um resumo em Markdown de todos os vídeos")
    a = ap.parse_args(argv)
    if a.roteiro and len(a.videos) > 1:
        ap.error("--roteiro só vale com um vídeo")

    partes, codigo = ["## ÍRIS", ""], 0
    for video in a.videos:
        pasta = Path(".iris") / video.stem
        extra = (["--roteiro", str(a.roteiro)] if a.roteiro else []) + \
                (["--referencia-voz", str(a.referencia_voz)] if a.referencia_voz else [])
        if inspecionar.main([str(video), "--saida", str(pasta), "--idioma", a.idioma, *extra]) != 0:
            codigo = 2
            partes.append(f"### {video.name}\n\nNão deu para inspecionar este vídeo.\n")
            continue
        if not a.sem_revisao:
            if revisar(video, pasta, a.revisao_em):
                print(f"revisão: {pasta / 'revisao.md'}")
            elif not shutil.which("claude"):
                print("Claude Code não encontrado: ficou só a inspeção (instale em https://claude.com/claude-code).")
            else:
                print("AVISO: o Claude Code rodou, mas não gravou revisao.json.", file=sys.stderr)
        partes.append(resumo(pasta))
    if a.resumo:
        a.resumo.write_text("\n".join(partes), encoding="utf-8")
        print(f"resumo:  {a.resumo}")
    return codigo


if __name__ == "__main__":
    sys.exit(main())
