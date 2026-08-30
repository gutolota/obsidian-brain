import importlib.util
import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "vault_report.py"


def run_report(vault: Path, *args: str):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(vault), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def test_report_counts_tasks_and_preserves_sources(tmp_path):
    vault = tmp_path / "vault"
    raw = vault / "1 - Notas brutas"
    complete = vault / "3 - Notas completas"
    raw.mkdir(parents=True)
    complete.mkdir(parents=True)
    source = raw / "Ideia.md"
    original = """---
type: fleeting
status: inbox
tags: [ideia]
---

Uma ideia sobre grafos e linguagem.

- [ ] Investigar benchmark
- [x] Ler introdução
"""
    source.write_text(original, encoding="utf-8")
    (complete / "Grafos.md").write_text("# Grafos\n\nVeja [[Ideia]].\n", encoding="utf-8")
    (raw / "Senha pessoal.md").write_text("senha: não-indexar\n- [ ] Tarefa privada\n", encoding="utf-8")
    (raw / "Conta.md").write_text("username: pessoa\npassword: segredo\n", encoding="utf-8")
    (raw / "Configuração.md").write_text("client_secret = exemplo-secreto-123456\n- [ ] Tarefa privada 2\n", encoding="utf-8")
    (raw / "Cabeçalhos.md").write_text("Authorization: Bearer exemplo-token-123456\n", encoding="utf-8")
    (raw / "Privada.md").write_text("---\nvisibility: private\n---\n- [ ] Tarefa privada 3\n", encoding="utf-8")

    payload = run_report(vault, "--write", "--json", str(tmp_path / "inventory.json"))

    assert payload["notes"] == 2
    assert payload["open_tasks"] == 1
    assert payload["done_tasks"] == 1
    assert source.read_text(encoding="utf-8") == original
    assert (vault / "Sistema" / "Resumo da vault.md").exists()
    assert (vault / "Sistema" / "Resumo de tarefas.md").exists()
    assert len(payload["written"]) == 5


def test_generated_task_report_keeps_source_links(tmp_path):
    vault = tmp_path / "vault"
    raw = vault / "1 - Notas brutas"
    raw.mkdir(parents=True)
    (raw / "Plano.md").write_text("- [ ] Fazer teste\n", encoding="utf-8")

    run_report(vault, "--write")
    report = (vault / "Sistema" / "Resumo de tarefas.md").read_text(encoding="utf-8")

    assert "Fazer teste" in report
    assert "[[1 - Notas brutas/Plano|Plano]]" in report
    assert "1 abertas" in report


def test_dry_run_writes_no_system_folder(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "Nota.md").write_text("# Nota\n", encoding="utf-8")

    payload = run_report(vault)

    assert payload["written"] == []
    assert not (vault / "Sistema").exists()


def test_system_folder_cannot_escape_vault(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "Nota.md").write_text("# Nota\n", encoding="utf-8")
    outside = tmp_path / "outside"

    traversal = subprocess.run(
        [sys.executable, str(SCRIPT), str(vault), "--write", "--system-folder", "../outside"],
        capture_output=True,
        text=True,
    )
    absolute = subprocess.run(
        [sys.executable, str(SCRIPT), str(vault), "--write", "--system-folder", str(outside)],
        capture_output=True,
        text=True,
    )

    assert traversal.returncode != 0
    assert absolute.returncode != 0
    assert not outside.exists()
