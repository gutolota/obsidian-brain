import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "knowledge_base.py"


def run_kb(db: Path, *args: str):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--db", str(db), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def test_hash_index_search_graph_and_secret_exclusion(tmp_path):
    vault = tmp_path / "vault"
    raw = vault / "1 - Notas brutas"
    raw.mkdir(parents=True)
    (raw / "Grafos.md").write_text(
        "# Grafos de conhecimento\n\nConstrução de grafos a partir de textos em português. Veja [[OpenIE]].\n",
        encoding="utf-8",
    )
    (raw / "OpenIE.md").write_text(
        "# OpenIE\n\nExtração aberta de relações e triplas.\n",
        encoding="utf-8",
    )
    (raw / "Senha pessoal.md").write_text("senha: não-indexar\n", encoding="utf-8")
    (raw / "Conta.md").write_text("username: pessoa\npassword: segredo\n", encoding="utf-8")
    db = tmp_path / "knowledge.db"

    built = run_kb(db, "build", str(vault), "--backend", "hash")
    searched = run_kb(db, "search", "grafos texto português", "--limit", "5")
    related = run_kb(db, "related", "Grafos", "--limit", "5")

    assert built["notes"] == 2
    assert built["edges"] == 1
    assert built["embedding_backend"] == "hash"
    assert searched["results"][0]["path"].endswith("Grafos.md")
    assert searched["results"][0]["absolute_path"].endswith("Grafos.md")
    assert "OpenIE" in related["outgoing"]
    assert all("Senha" not in row["path"] for row in searched["results"])


def test_stats_reports_embedding_metadata(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "Nota.md").write_text("# Nota\n\nconteúdo", encoding="utf-8")
    db = tmp_path / "knowledge.db"

    run_kb(db, "build", str(vault), "--backend", "hash")
    stats = run_kb(db, "stats")

    assert stats["notes"] == 1
    assert stats["embedding_model"] == "deterministic-hash"
    assert stats["embedding_dimensions"] == "1024"
