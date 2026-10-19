"""Adaptador ComfyUI contra um servidor falso (sem ComfyUI instalado)."""
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from iris import comfyui  # noqa: E402

RECEBIDOS = []


class FalsoComfy(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _json(self, dados):
        corpo = json.dumps(dados).encode()
        self.send_response(200)
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_POST(self):
        RECEBIDOS.append(json.loads(self.rfile.read(int(self.headers["Content-Length"]))))
        self._json({"prompt_id": f"p{len(RECEBIDOS)}"})

    def do_GET(self):
        if self.path.startswith("/history/"):
            pid = self.path.rsplit("/", 1)[1]
            self._json({pid: {"outputs": {"9": {"gifs": [{"filename": f"{pid}.mp4", "subfolder": "", "type": "output"}],
                                                "images": [{"filename": "x.png", "type": "temp"}]}}}})
        else:
            corpo = self.path.encode()
            self.send_response(200)
            self.send_header("Content-Length", str(len(corpo)))
            self.end_headers()
            self.wfile.write(corpo)


def test_preencher_troca_marcadores():
    wf = {"3": {"inputs": {"seed": "{{seed}}", "text": "foto: {{prompt}}", "prefixo": "{{nome}}"}}}
    assert comfyui.preencher(wf, {"prompt": "uma águia", "seed": 42, "nome": "cena_2"}) == \
        {"3": {"inputs": {"seed": 42, "text": "foto: uma águia", "prefixo": "cena_2"}}}


def test_refaz_so_as_cenas_pedidas(tmp_path):
    servidor = HTTPServer(("127.0.0.1", 0), FalsoComfy)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    try:
        (tmp_path / "revisao.json").write_text(json.dumps({"refazer": [
            {"cena": 2, "motivo": "bola some", "ajuste_prompt": "ball stays in frame"}, {"cena": 3}]}), encoding="utf-8")
        (tmp_path / "roteiro.json").write_text(json.dumps({"cenas": [
            {"prompt": "a"}, {"prompt": "tennis ball"}, {"narracao": "fim"}]}), encoding="utf-8")
        (tmp_path / "wf.json").write_text(json.dumps({"1": {"inputs": {"text": "{{prompt}}", "seed": "{{seed}}"}}}),
                                          encoding="utf-8")
        RECEBIDOS.clear()
        assert comfyui.main([str(tmp_path / "revisao.json"), "--roteiro", str(tmp_path / "roteiro.json"),
                             "--workflow", str(tmp_path / "wf.json"), "--max-refazer", "1",
                             "--servidor", f"http://127.0.0.1:{servidor.server_port}"]) == 0
    finally:
        servidor.shutdown()
    assert len(RECEBIDOS) == 1                                       # --max-refazer 1
    entradas = RECEBIDOS[0]["prompt"]["1"]["inputs"]
    assert entradas["text"] == "tennis ball, ball stays in frame" and isinstance(entradas["seed"], int)
    manifesto = json.loads((tmp_path / "refeitas" / "manifesto.json").read_text(encoding="utf-8"))
    assert manifesto[0]["cena"] == 2 and manifesto[0]["arquivos"] == ["cena_2.mp4"]
    assert b"filename=p1.mp4" in (tmp_path / "refeitas" / "cena_2.mp4").read_bytes()   # a imagem "temp" ficou de fora
