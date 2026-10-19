"""Testes da linha de comando (python -m iris) com o vídeo sintético dos testes do inspetor."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import iris.__main__ as cli  # noqa: E402
from test_inspecionar import pytestmark, video  # noqa: E402,F401


def test_sem_revisao_grava_medidas_e_resumo(video, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert cli.main([str(video), "--sem-revisao", "--resumo", "r.md"]) == 0
    assert (tmp_path / ".iris" / "teste" / "medidas.json").exists()
    texto = (tmp_path / "r.md").read_text(encoding="utf-8")
    assert "### teste.mp4" in texto and "Só as medidas automáticas" in texto


def test_resumo_com_revisao(video, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cli.main([str(video), "--sem-revisao"])
    pasta = tmp_path / ".iris" / "teste"
    (pasta / "revisao.json").write_text(json.dumps({
        "nota": 6.5, "resumo": "bola some",
        "problemas": [{"segundo": 47.5, "tipo": "visual", "gravidade": "alta", "descricao": "bola | some"}],
        "refazer": [{"cena": 3, "motivo": "bola some"}]}), encoding="utf-8")
    texto = cli.resumo(pasta)
    assert "**Nota 6.5**" in texto and "| 0:47.5 | visual | alta | bola / some |" in texto
    assert "cena 3 (bola some)" in texto


def test_sem_claude_fica_so_a_inspecao(video, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(cli.shutil, "which", lambda nome: None if nome == "claude" else "x")
    assert cli.revisar(video, tmp_path) is False


def test_video_inexistente_devolve_2(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert cli.main([str(tmp_path / "nada.mp4"), "--sem-revisao", "--resumo", "r.md"]) == 2
    assert "Não deu para inspecionar" in (tmp_path / "r.md").read_text(encoding="utf-8")
