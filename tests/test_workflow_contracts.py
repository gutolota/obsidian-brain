from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_refinement_creates_additive_complete_note_drafts():
    refine = (ROOT / ".agents/skills/obsidian-brain-refine/SKILL.md").read_text(encoding="utf-8")
    triage = (ROOT / ".agents/skills/obsidian-brain-triage/SKILL.md").read_text(encoding="utf-8")

    assert "3 - Notas completas/_Rascunhos/" in refine
    assert "status: draft" in refine
    assert "leaves sources untouched" in refine
    assert "configured batch size" in triage
    assert "needs no approval" in triage
    assert "Sistema/Rascunhos de lapidação/" not in refine


def test_task_workflows_use_live_dashboard_without_static_copies():
    agenda = (ROOT / ".agents/skills/obsidian-brain-agenda/SKILL.md").read_text(encoding="utf-8")
    weekly = (ROOT / ".agents/skills/obsidian-brain-weekly-review/SKILL.md").read_text(encoding="utf-8")
    reporter = (ROOT / "scripts/vault_report.py").read_text(encoding="utf-8")

    assert "Dataview dashboard" in agenda
    assert "Do not generate or copy a static task list" in agenda
    assert "never copy them into the weekly report" in weekly
    assert '"Resumo de tarefas.md"' not in reporter


def test_modified_agent_and_claude_skills_are_synchronized():
    names = [
        "obsidian-brain-agenda",
        "obsidian-brain-refine",
        "obsidian-brain-triage",
        "obsidian-brain-weekly-review",
    ]
    for name in names:
        agent = (ROOT / ".agents/skills" / name / "SKILL.md").read_bytes()
        claude = (ROOT / ".claude/skills" / name / "SKILL.md").read_bytes()
        assert agent == claude


def test_daily_template_and_plugin_contract_share_task_format():
    daily = (ROOT / "templates/vault/diario.md").read_text(encoding="utf-8")
    dashboard = (ROOT / "templates/vault/tarefas.md").read_text(encoding="utf-8")
    policy = (ROOT / "data/plugin-integration.md").read_text(encoding="utf-8")

    assert "## Sessions" in daily
    assert "## Tasks" in daily
    assert "📅 YYYY-MM-DD" in daily
    assert "Diário/" in dashboard
    assert "Global filter is empty" in policy
    assert "`#task` is not required" in policy
    assert "Dataview dashboard" in policy


def test_idea_mvp_and_indexes_contract():
    mvp = (ROOT / ".agents/skills/obsidian-brain-mvp/SKILL.md").read_text(encoding="utf-8")
    ideas = (ROOT / "templates/vault/ideias.md").read_text(encoding="utf-8")
    tags = (ROOT / "templates/vault/tags.md").read_text(encoding="utf-8")
    sync = (ROOT / "scripts/obsidian_kanban_sync.py").read_text(encoding="utf-8")

    assert "Projects/MVPs/<slug>/MVP.md" in mvp
    assert "success metric" in mvp
    assert "Hermes Kanban is available" in mvp
    assert 'FROM "Projects/MVPs"' in ideas
    assert "FLATTEN file.tags" in tags
    assert "read-only Obsidian Markdown board" in sync
