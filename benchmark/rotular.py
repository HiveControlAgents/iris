"""Página local para rotular os achados da ÍRIS: assiste ao trecho, clica Certo ou Errado, anota o que ela não viu.

    python benchmark/rotular.py --videos PASTA_DOS_VIDEOS [--porta 8765] [--sem-navegador]

Sobe um servidor só em 127.0.0.1 e abre o navegador. Os vídeos são achados em PASTA_DOS_VIDEOS pelo mesmo id que
`bench.py pasta` usa (o nome da pasta de cada vídeo) e servidos direto do disco: nunca vão para o repositório.
Cada clique grava em benchmark/rotulos/<id>.md, no formato que `bench.py metricas` lê.
Só atende a própria página: outro site aberto no navegador não consegue ler nem gravar os rótulos.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bench  # noqa: E402

TEMPO = re.compile(r"^(\d+):(\d+(?:[.,]\d+)?)$")


def _segundos(texto: str):
    m = TEMPO.match(texto.strip())
    return int(m.group(1)) * 60 + float(m.group(2).replace(",", ".")) if m else None


def ler(arq: Path) -> dict:
    """Achados (com o rótulo atual) e defeitos que a ÍRIS não viu, lidos do arquivo de rótulos."""
    achados, perdidos, secao = [], [], ""
    for linha in arq.read_text(encoding="utf-8").splitlines():
        if linha.startswith("## "):
            secao = "perdidos" if "não viu" in linha or "Missed" in linha else "achados"
            continue
        m = bench.MARCA_ROTULO.match(linha.strip())
        if m:
            partes = [p.strip() for p in m.group(3).split("|", 3)] + ["", "", "", ""]
            certo, errado = m.group(1) != " ", m.group(2) != " "
            achados.append({"i": len(achados), "tempo": partes[0], "segundo": _segundos(partes[0]),
                            "tipo": partes[1], "gravidade": partes[2], "descricao": partes[3],
                            "rotulo": "certo" if certo and not errado else "errado" if errado and not certo else None})
        elif secao == "perdidos" and linha.startswith("- "):
            perdidos.append(linha[2:])
    return {"achados": achados, "perdidos": perdidos}


def marcar(arq: Path, i: int, valor: str) -> None:
    """Marca o achado número i (0 = o primeiro) como 'certo', 'errado' ou '' (desmarcar)."""
    linhas, n = arq.read_text(encoding="utf-8").splitlines(), -1
    for k, linha in enumerate(linhas):
        m = bench.MARCA_ROTULO.match(linha.strip())
        if m:
            n += 1
            if n == i:
                c, e = ("x" if valor == "certo" else " "), ("x" if valor == "errado" else " ")
                linhas[k] = f"- [{c}] certo  [{e}] errado | {m.group(3)}"
                arq.write_text("\n".join(linhas) + "\n", encoding="utf-8")
                return
    raise IndexError(f"achado {i} não existe em {arq.name}")


def anotar_perdido(arq: Path, texto: str, segundo: str = "") -> None:
    """Acrescenta um defeito que a ÍRIS não viu no fim da seção de perdidos (que é a última do arquivo)."""
    texto = " ".join(texto.split()).replace("|", "/")
    if not texto:
        raise ValueError("texto vazio")
    linha = f"- {segundo.strip() or '?'} | {texto}"
    arq.write_text(arq.read_text(encoding="utf-8").rstrip("\n") + "\n" + linha + "\n", encoding="utf-8")


def dados(locais: dict[str, Path]) -> list[dict]:
    videos = []
    for v in bench._ler(bench.VIDEOS, []):
        arq = bench.ROTULOS / f"{v['id']}.md"
        if arq.exists():
            videos.append({"id": v["id"], "titulo": v["titulo"], "tem_video": v["id"] in locais, **ler(arq)})
    return videos


def achar_videos(pasta: Path | None, padrao: str = "*/video*.mp4") -> dict[str, Path]:
    return {bench.id_do_video(v): v for v in sorted(pasta.glob(padrao))} if pasta else {}


class Pagina(BaseHTTPRequestHandler):
    locais: dict[str, Path] = {}

    def log_message(self, *a):
        pass

    def _enviar(self, codigo: int, corpo: bytes, tipo: str, extra: dict | None = None):
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(corpo)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(corpo)

    def _json(self, dados, codigo=200):
        self._enviar(codigo, json.dumps(dados, ensure_ascii=False).encode(), "application/json; charset=utf-8")

    def _de_fora(self) -> bool:
        """Pedido que não veio desta página: Host de outro nome (DNS rebinding) ou POST com Origin de outro site."""
        locais = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
        if self.headers.get("Host", "").lower() not in locais:
            return True
        origem = self.headers.get("Origin")   # sem Origin (curl, testes) passa: navegador sempre manda no POST
        return self.command == "POST" and origem is not None and origem.lower() not in {f"http://{h}" for h in locais}

    def do_GET(self):
        if self._de_fora():
            return self._json({"erro": "pedido de fora da página local"}, 403)
        if self.path == "/":
            return self._enviar(200, HTML.encode(), "text/html; charset=utf-8")
        if self.path == "/api/dados":
            return self._json(dados(self.locais))
        if self.path.startswith("/video/"):
            return self._video(self.path[len("/video/"):])
        self._enviar(404, b"", "text/plain")

    def _video(self, ident: str):
        """Serve o arquivo com Range, para o navegador conseguir pular para o segundo do achado."""
        arq = self.locais.get(ident)
        if not arq:
            return self._enviar(404, b"", "text/plain")
        total = arq.stat().st_size
        m = re.match(r"bytes=(\d*)-(\d*)", self.headers.get("Range", ""))
        ini, fim = 0, total - 1
        if m:
            ini = int(m.group(1)) if m.group(1) else total - int(m.group(2))
            fim = int(m.group(2)) if m.group(1) and m.group(2) else total - 1
            fim = min(fim, ini + 8 * 2**20 - 1, total - 1)   # pedaços de até 8 MB
        with open(arq, "rb") as f:
            f.seek(ini)
            corpo = f.read(fim - ini + 1)
        extra = {"Accept-Ranges": "bytes"}
        if m:
            extra["Content-Range"] = f"bytes {ini}-{fim}/{total}"
        self._enviar(206 if m else 200, corpo, "video/mp4", extra)

    def do_POST(self):
        if self._de_fora():
            return self._json({"erro": "pedido de fora da página local"}, 403)
        try:
            pedido = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            ident = bench.slug(str(pedido.get("id", "")))
            arq = bench.ROTULOS / f"{ident}.md"
            if not ident or not arq.exists():
                return self._json({"erro": "vídeo desconhecido"}, 404)
            if self.path == "/api/rotulo" and pedido.get("valor") in ("certo", "errado", ""):
                marcar(arq, int(pedido["i"]), pedido["valor"])
            elif self.path == "/api/perdido":
                anotar_perdido(arq, str(pedido.get("texto", "")), str(pedido.get("segundo", "")))
            else:
                return self._json({"erro": "pedido inválido"}, 400)
            self._json(ler(arq))
        except (ValueError, IndexError, KeyError) as e:
            self._json({"erro": str(e)}, 400)


HTML = r"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Rotular achados da ÍRIS</title>
<style>
body{font:15px/1.45 system-ui,sans-serif;margin:0;background:#f4f4f2;color:#222}
header{position:sticky;top:0;background:#222;color:#fff;padding:10px 20px;display:flex;gap:20px;align-items:center;z-index:2}
header b{font-size:17px} #barra{flex:1;height:8px;background:#555;border-radius:4px;overflow:hidden}
#barra i{display:block;height:100%;background:#f5c400;width:0}
main{display:grid;grid-template-columns:360px 1fr;gap:20px;padding:20px;max-width:1300px;margin:auto}
#lado{position:sticky;top:60px;align-self:start} video{width:100%;max-height:70vh;background:#000;border-radius:6px}
select{width:100%;padding:6px;margin-bottom:10px;font-size:15px}
.achado{background:#fff;border-radius:6px;padding:10px 12px;margin-bottom:8px;border-left:5px solid #ccc}
.achado.certo{border-color:#2a9d4b}.achado.errado{border-color:#d33}
.meta{font-size:13px;color:#666;margin-bottom:4px} .meta b{color:#222}
button{font-size:14px;padding:5px 12px;margin-right:6px;border:1px solid #bbb;border-radius:4px;background:#fafafa;cursor:pointer}
button.ok.on{background:#2a9d4b;color:#fff;border-color:#2a9d4b} button.no.on{background:#d33;color:#fff;border-color:#d33}
.perdidos{background:#fff;border-radius:6px;padding:12px;margin-top:16px}
.perdidos input{padding:6px;font-size:14px} .perdidos li{margin:3px 0}
.aviso{color:#a60;font-size:13px}
</style></head><body>
<header><b>ÍRIS: rotular achados</b><span id="prog"></span><div id="barra"><i></i></div></header>
<main><div id="lado"><select id="escolha"></select><video id="v" controls preload="metadata"></video>
<p class="aviso" id="semvideo" hidden>Arquivo deste vídeo não encontrado na pasta informada.</p>
<p style="font-size:13px;color:#666">Clique em ▶ para ver o trecho a partir de 2 s antes do achado. Cada clique já fica salvo.</p></div>
<div><div id="lista"></div>
<div class="perdidos"><b>O que a ÍRIS não viu</b><ul id="perd"></ul>
<input id="seg" placeholder="segundo (ex. 0:30)" size="14"> <input id="txt" placeholder="o que está errado no vídeo" size="50">
<button id="add">Adicionar</button></div></div></main>
<script>
let videos=[], atual=0;
const $=s=>document.querySelector(s);
async function api(url, corpo){const r=await fetch(url,corpo?{method:"POST",body:JSON.stringify(corpo)}:{});return r.json()}
function progresso(){let t=0,f=0;videos.forEach(v=>v.achados.forEach(a=>{t++;if(a.rotulo)f++}));
 $("#prog").textContent=`${f} de ${t} achados rotulados`;$("#barra i").style.width=(t?100*f/t:0)+"%"}
function tocar(seg){const v=$("#v");if(seg==null)return;v.currentTime=Math.max(0,seg-2);v.play()}
function desenhar(){const v=videos[atual];if(!v)return;
 $("#semvideo").hidden=v.tem_video; $("#v").src=v.tem_video?"/video/"+encodeURIComponent(v.id):"";
 $("#lista").innerHTML="";
 v.achados.forEach(a=>{const d=document.createElement("div");d.className="achado "+(a.rotulo||"");
  d.innerHTML=`<div class="meta"><b>${a.tempo}</b> · ${a.tipo} · ${a.gravidade}</div><div></div><div style="margin-top:6px">
  <button class="ver">▶ ver</button><button class="ok ${a.rotulo=="certo"?"on":""}">Certo</button>
  <button class="no ${a.rotulo=="errado"?"on":""}">Errado</button></div>`;
  d.children[1].textContent=a.descricao;
  d.querySelector(".ver").onclick=()=>tocar(a.segundo);
  d.querySelector(".ok").onclick=()=>rotular(a,a.rotulo=="certo"?"":"certo");
  d.querySelector(".no").onclick=()=>rotular(a,a.rotulo=="errado"?"":"errado");
  $("#lista").appendChild(d)});
 $("#perd").innerHTML="";v.perdidos.forEach(p=>{const li=document.createElement("li");li.textContent=p;$("#perd").appendChild(li)});
 progresso()}
async function rotular(a,valor){const v=videos[atual];const r=await api("/api/rotulo",{id:v.id,i:a.i,valor});
 if(r.erro)return alert(r.erro);Object.assign(v,r);desenhar()}
$("#add").onclick=async()=>{const v=videos[atual];const r=await api("/api/perdido",{id:v.id,texto:$("#txt").value,segundo:$("#seg").value});
 if(r.erro)return alert(r.erro);Object.assign(v,r);$("#txt").value="";$("#seg").value="";desenhar()};
$("#escolha").onchange=e=>{atual=+e.target.value;desenhar()};
api("/api/dados").then(d=>{videos=d;d.forEach((v,k)=>{const o=document.createElement("option");o.value=k;
 o.textContent=`${v.titulo} (${v.achados.length} achados)`;$("#escolha").appendChild(o)});desenhar()});
</script></body></html>"""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="rotular.py", description="Página local para rotular os achados da ÍRIS.")
    ap.add_argument("--videos", type=Path, help="pasta com os vídeos (uma subpasta por vídeo, como em bench.py pasta)")
    ap.add_argument("--padrao", default="*/video*.mp4")
    ap.add_argument("--porta", type=int, default=8765)
    ap.add_argument("--sem-navegador", action="store_true")
    a = ap.parse_args(argv)
    Pagina.locais = achar_videos(a.videos, a.padrao)
    servidor = ThreadingHTTPServer(("127.0.0.1", a.porta), Pagina)
    url = f"http://127.0.0.1:{a.porta}/"
    faltando = [v["id"] for v in dados(Pagina.locais) if not v["tem_video"]]
    print(f"rotular: {url}" + (f" (sem arquivo de vídeo: {', '.join(faltando)})" if faltando else ""))
    if not a.sem_navegador:
        threading.Timer(0.5, webbrowser.open, [url]).start()
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
