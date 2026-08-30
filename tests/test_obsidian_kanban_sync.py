import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts/obsidian_kanban_sync.py"


def load_sync():
    spec = importlib.util.spec_from_file_location("obsidian_kanban_sync", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_output_must_remain_inside_vault(tmp_path):
    sync = load_sync()
    vault = tmp_path / "vault"
    vault.mkdir()

    assert sync.resolve_output(vault, Path("Indexes/Kanban Hermes.md")) == (
        vault / "Indexes/Kanban Hermes.md"
    )
    with pytest.raises(ValueError):
        sync.resolve_output(vault, Path("../outside.md"))
    with pytest.raises(ValueError):
        sync.resolve_output(vault, tmp_path / "absolute.md")


def test_output_rejects_symlink_escape(tmp_path):
    sync = load_sync()
    vault = tmp_path / "vault"
    outside = tmp_path / "outside"
    vault.mkdir()
    outside.mkdir()
    (vault / "Indexes").symlink_to(outside, target_is_directory=True)

    with pytest.raises(ValueError):
        sync.resolve_output(vault, Path("Indexes/Kanban Hermes.md"))


def test_render_is_read_only_and_escapes_untrusted_fields():
    sync = load_sync()
    rendered = sync.render(
        [
            {
                "id": "id-->hidden`",
                "title": "[Injected](https://example.invalid)\n## heading",
                "status": "todo",
                "assignee": "person`code",
                "priority": "high",
            }
        ],
        'default\nmalicious: "value"',
    )

    assert "- [ ]" not in rendered
    assert "- [x]" not in rendered
    assert "<!--" not in rendered
    assert 'hermes_board: "default malicious: \\"value\\""' in rendered
    assert "\\[Injected\\]\\(https://example\\.invalid\\)" in rendered
    assert "person'code" in rendered


def test_nonnumeric_priority_does_not_break_sorting():
    sync = load_sync()
    rendered = sync.render(
        [
            {"id": "low", "title": "Low", "status": "todo", "priority": "low"},
            {"id": "high", "title": "High", "status": "todo", "priority": "high"},
            {"id": "other", "title": "Other", "status": "todo", "priority": "not-a-number"},
        ],
        "default",
    )

    assert rendered.index("High") < rendered.index("Low") < rendered.index("Other")
