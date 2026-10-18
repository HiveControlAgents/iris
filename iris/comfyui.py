"""Adaptador ComfyUI (local, de graça) para o ciclo revisar e refazer: gera de novo só as cenas que a ÍRIS pediu.

    python -m iris.comfyui .iris/<video>/revisao.json --roteiro roteiro.json --workflow meu_workflow_api.json

- `--workflow`: o seu workflow exportado no ComfyUI com "Save (API Format)". Nos campos de texto e de semente,
  escreva os marcadores: "{{prompt}}" (o prompt da cena, com o ajuste sugerido pela ÍRIS), "{{seed}}" (vira um
  número novo a cada cena) e, se quiser, "{{nome}}" (prefixo do arquivo, por exemplo no SaveImage/VHS_VideoCombine).
- O prompt de cada cena vem do roteiro (`prompt_video`, `prompt` ou `narracao`, nessa ordem).
- Saída: `<pasta da revisão>/refeitas/cena_N.<ext>` e `refeitas/manifesto.json`. Remontar o vídeo final fica com o
  seu pipeline: troque os clipes das cenas refeitas e rode a ÍRIS de novo com `rodada: 2`.

Só usa a biblioteca padrão. Outros geradores (Kling, Runway, Veo...) entram com a mesma interface de
`refazer_cena`: veja docs/adaptadores.md.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
import urllib.parse
import urllib.request
import uuid
from pathlib import Path


def preencher(no, valores: dict):
    """Troca os marcadores {{chave}} em todo o workflow. Um campo que é só "{{seed}}" vira número."""
    if isinstance(no, dict):
        return {k: preencher(v, valores) for k, v in no.items()}
    if isinstance(no, list):
        return [preencher(v, valores) for v in no]
    if isinstance(no, str):
        for chave, valor in valores.items():
            if no == "{{" + chave + "}}" and isinstance(valor, int):
                return valor
            no = no.replace("{{" + chave + "}}", str(valor))
    return no


def _pedir(url: str, dados: dict | None = None):
    corpo = json.dumps(dados).encode() if dados is not None else None
    req = urllib.request.Request(url, data=corpo, headers={"Content-Type": "application/json"} if corpo else {})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def refazer_cena(servidor: str, workflow: dict, prompt: str, semente: int, nome: str, destino: Path,
                 espera_max_s: int = 3600) -> list[Path]:
    """Manda o workflow preenchido para a fila do ComfyUI, espera terminar e baixa os arquivos gerados."""
    cliente = uuid.uuid4().hex
    preenchido = preencher(workflow, {"prompt": prompt, "seed": semente, "nome": nome})
    pedido = json.loads(_pedir(f"{servidor}/prompt", {"prompt": preenchido, "client_id": cliente}))
    pid, limite = pedido["prompt_id"], time.time() + espera_max_s
    while True:
        historico = json.loads(_pedir(f"{servidor}/history/{pid}")).get(pid)
        if historico and historico.get("outputs"):
            break
        if historico and historico.get("status", {}).get("status_str") == "error":
            raise RuntimeError(f"o ComfyUI deu erro na cena {nome}")
        if time.time() > limite:
            raise TimeoutError(f"o ComfyUI não terminou a cena {nome} em {espera_max_s} s")
        time.sleep(2)
    salvos = []
    for saida in historico["outputs"].values():
        for item in [i for lista in saida.values() if isinstance(lista, list) for i in lista if isinstance(i, dict)]:
            if "filename" not in item or item.get("type") == "temp":
                continue
            consulta = urllib.parse.urlencode({k: item.get(k, "") for k in ("filename", "subfolder", "type")})
            arq = destino / f"{nome}{Path(item['filename']).suffix}"
            if arq.exists():                               # mais de um arquivo na mesma cena
                arq = destino / f"{nome}_{len(salvos)}{Path(item['filename']).suffix}"
            arq.write_bytes(_pedir(f"{servidor}/view?{consulta}"))
            salvos.append(arq)
    return salvos


def prompt_da_cena(roteiro: dict, n: int, ajuste: str) -> str:
    cenas = roteiro.get("cenas") or []
    cena = cenas[n - 1] if 0 < n <= len(cenas) else {}
    base = cena.get("prompt_video") or cena.get("prompt") or cena.get("narracao") or ""
    return f"{base}, {ajuste}".strip(", ") if ajuste else base


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m iris.comfyui", description="Refaz no ComfyUI as cenas que a ÍRIS pediu.")
    ap.add_argument("revisao", type=Path, help="revisao.json da ÍRIS")
    ap.add_argument("--roteiro", type=Path, required=True, help="roteiro com o prompt de cada cena")
    ap.add_argument("--workflow", type=Path, required=True, help="workflow do ComfyUI em formato API, com marcadores")
    ap.add_argument("--servidor", default="http://127.0.0.1:8188", help="endereço do ComfyUI (padrão: local)")
    ap.add_argument("--max-refazer", type=int, default=3, help="máximo de cenas (padrão: 3)")
    a = ap.parse_args(argv)

    revisao = json.loads(a.revisao.read_text(encoding="utf-8"))
    roteiro = json.loads(a.roteiro.read_text(encoding="utf-8"))
    workflow = json.loads(a.workflow.read_text(encoding="utf-8"))
    pedidos = (revisao.get("refazer") or [])[:a.max_refazer]
    if not pedidos:
        print("A revisão não pediu para refazer nenhuma cena.")
        return 0
    destino = a.revisao.parent / "refeitas"
    destino.mkdir(exist_ok=True)
    manifesto = []
    for p in pedidos:
        n = int(p["cena"])
        prompt, semente = prompt_da_cena(roteiro, n, p.get("ajuste_prompt", "")), random.randint(1, 2**31 - 1)
        print(f"cena {n}: semente {semente}")
        arquivos = refazer_cena(a.servidor.rstrip("/"), workflow, prompt, semente, f"cena_{n}", destino)
        manifesto.append({"cena": n, "semente": semente, "prompt": prompt, "motivo": p.get("motivo", ""),
                          "arquivos": [f.name for f in arquivos]})
    (destino / "manifesto.json").write_text(json.dumps(manifesto, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"refeitas: {destino}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
