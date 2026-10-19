"""Benchmark: rótulos, métricas, tabela e limpeza de caminhos (sem rodar revisão de verdade)."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "benchmark"))
import bench  # noqa: E402


@pytest.fixture
def base(tmp_path, monkeypatch):
    for nome, valor in {"RESULTADOS": tmp_path / "resultados", "ROTULOS": tmp_path / "rotulos",
                        "VIDEOS": tmp_path / "videos.json", "LEIAME": tmp_path / "README.md",
                        "DEFEITOS": tmp_path / "defeitos.csv"}.items():
        monkeypatch.setattr(bench, nome, valor)
    (tmp_path / "README.md").write_text("# B\n\n<!-- tabela:inicio -->\nvelha\n<!-- tabela:fim -->\n", encoding="utf-8")
    pasta = tmp_path / "resultados" / "tenis-v3"
    pasta.mkdir(parents=True)
    (pasta / "revisao.json").write_text(json.dumps({"nota": 5.5, "problemas": [
        {"segundo": 47.0, "tipo": "visual", "gravidade": "alta", "descricao": "bola surge | no ar"},
        {"segundo": 13.0, "tipo": "legenda", "gravidade": "media", "descricao": "legenda transparente"},
        {"segundo": 2.0, "tipo": "audio", "gravidade": "baixa", "descricao": "volume baixo"}]}), encoding="utf-8")
    (tmp_path / "videos.json").write_text(json.dumps([{"id": "tenis-v3", "titulo": "Tênis v3", "link": ""}]),
                                          encoding="utf-8")
    return tmp_path


def test_tabela_conta_por_tipo_com_segundos(base):
    bench.tabela()
    texto = (base / "README.md").read_text(encoding="utf-8")
    assert "velha" not in texto
    assert "| Tênis v3 | 5.5 | 3 | 1 | 0 | 0 | 1 | 1 | 0 | 0:47.0 visual; 0:13.0 legenda; 0:02.0 audio |" in texto
    assert (base / "defeitos.csv").read_text(encoding="utf-8").count("tenis-v3,") == 3


def test_rotulos_e_metricas(base):
    arq = bench.criar_rotulos("tenis-v3", "Tênis v3")
    texto = arq.read_text(encoding="utf-8")
    assert texto.count("- [ ] certo  [ ] errado |") == 3 and "bola surge / no ar" in texto
    assert bench.metricas()["videos"] == 0                    # nada marcado ainda: fica pendente
    marcas = iter(["[x] certo  [ ] errado", "[x] certo  [ ] errado", "[ ] certo  [x] errado"])
    linhas = [f"- {next(marcas)} |{ln.split('|', 1)[1]}" if ln.startswith("- [ ] certo") else ln
              for ln in texto.splitlines()]
    linhas.append("- 0:30 | visual | mão com seis dedos")
    arq.write_text("\n".join(linhas), encoding="utf-8")
    assert bench.ler_rotulos(arq) == {"certos": 2, "errados": 1, "pendentes": 0, "perdidos": 1}
    m = bench.metricas()
    assert m["videos"] == 1 and m["precisao"] == round(2 / 3, 3) and m["revocacao"] == round(2 / 3, 3)
    assert "| 1 (pendentes: 0) | 67% | 67% | 2 | 1 | 1 |" in (base / "README.md").read_text(encoding="utf-8")
    bench.criar_rotulos("tenis-v3", "Tênis v3")               # não apaga o que já foi rotulado
    assert "seis dedos" in arq.read_text(encoding="utf-8")


def test_limpa_caminhos_do_disco():
    texto = r'vídeo em C:\Users\fulano\Videos\a.mp4 e /home/fulano/b.mp4, ver "D:/x/y.json" e https://github.com/a'
    limpo = bench.limpar_caminhos(texto)
    assert "fulano" not in limpo and "D:/x" not in limpo and "https://github.com/a" in limpo


def test_slug():
    assert bench.slug("2026-10-12-v4_Por que os TENISTAS veem a bola?") == "2026-10-12-v4-por-que-os-tenistas-veem-a-bola"
