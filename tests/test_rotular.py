"""Página de rotulação: grava no formato que bench.metricas lê e serve vídeo com Range."""
import json
import sys
import threading
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "benchmark"))
import bench  # noqa: E402
import rotular  # noqa: E402
from test_bench import base  # noqa: E402,F401


def test_marcar_e_anotar_perdido(base):
    arq = bench.criar_rotulos("tenis-v3", "Tênis v3")
    rotular.marcar(arq, 0, "certo")
    rotular.marcar(arq, 2, "errado")
    rotular.marcar(arq, 2, "certo")                           # trocar de ideia sobrescreve
    rotular.anotar_perdido(arq, "mão com | seis dedos", "0:30")
    d = rotular.ler(arq)
    assert [a["rotulo"] for a in d["achados"]] == ["certo", None, "certo"]
    assert d["achados"][0]["segundo"] == 47.0 and d["perdidos"] == ["0:30 | mão com / seis dedos"]
    assert bench.ler_rotulos(arq) == {"certos": 2, "errados": 0, "pendentes": 1, "perdidos": 1}
    rotular.marcar(arq, 1, "errado")
    assert bench.metricas()["precisao"] == round(2 / 3, 3)


def test_servidor_rotula_e_serve_video_com_range(base, tmp_path):
    bench.criar_rotulos("tenis-v3", "Tênis v3")
    video = tmp_path / "saida" / "tenis-v3" / "video.mp4"
    video.parent.mkdir(parents=True)
    video.write_bytes(bytes(range(256)) * 4)
    rotular.Pagina.locais = rotular.achar_videos(tmp_path / "saida")
    servidor = ThreadingHTTPServer(("127.0.0.1", 0), rotular.Pagina)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{servidor.server_port}"
    try:
        [v] = json.loads(urllib.request.urlopen(url + "/api/dados").read())
        assert v["tem_video"] and len(v["achados"]) == 3
        pedido = urllib.request.Request(url + "/api/rotulo", data=json.dumps({"id": "tenis-v3", "i": 1, "valor": "errado"}).encode())
        assert json.loads(urllib.request.urlopen(pedido).read())["achados"][1]["rotulo"] == "errado"
        r = urllib.request.urlopen(urllib.request.Request(url + "/video/tenis-v3", headers={"Range": "bytes=10-19"}))
        assert r.status == 206 and r.read() == bytes(range(10, 20)) and r.headers["Content-Range"] == "bytes 10-19/1024"
        assert "ÍRIS" in urllib.request.urlopen(url + "/").read().decode()
    finally:
        servidor.shutdown()
