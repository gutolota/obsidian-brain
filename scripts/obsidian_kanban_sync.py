#!/usr/bin/env python3
"""Render Hermes Kanban as a read-only Obsidian Markdown board."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

STATUS_ORDER = ["triage", "todo", "ready", "running", "blocked", "review", "done"]
STATUS_LABELS = {
    "triage": "Triagem",
    "todo": "A fazer",
    "ready": "Prontas",
    "running": "Em andamento",
    "blocked": "Bloqueadas",
    "review": "Revisão",
    "done": "Concluídas",
    "scheduled": "Agendadas",
}
PRIORITY_NAMES = {"critical": 4, "urgent": 4, "high": 3, "medium": 2, "normal": 2, "low": 1}


def fetch_tasks(hermes: str, board: str | None) -> list[dict]:
    command = [hermes, "kanban"]
    if board:
        command.extend(["--board", board])
    command.extend(["list", "--json", "--archived"])
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    payload = json.loads(completed.stdout or "[]")
    if isinstance(payload, dict):
        payload = payload.get("tasks", payload.get("items", []))
    if not isinstance(payload, list):
        raise ValueError("Unexpected Hermes Kanban JSON payload")
    return [item for item in payload if isinstance(item, dict)]


def safe_text(value: object) -> str:
    """Collapse untrusted card values to one printable line."""
    text = str(value or "").replace("\n", " ").replace("\r", " ")
    return "".join(char for char in text if char.isprintable()).strip()


def markdown_text(value: object) -> str:
    text = safe_text(value)
    for char in "\\`*_{}[]<>()#+-.!|":
        text = text.replace(char, f"\\{char}")
    return text


def code_text(value: object) -> str:
    return safe_text(value).replace("`", "'")


def priority_value(value: object) -> int:
    if value in (None, ""):
        return 0
    try:
        return int(safe_text(value))
    except (TypeError, ValueError):
        return PRIORITY_NAMES.get(safe_text(value).lower(), 0)


def resolve_output(vault: Path, output: Path) -> Path:
    """Resolve a relative output inside the vault without symlink escape."""
    if output.is_absolute() or ".." in output.parts:
        raise ValueError("--output must be a relative path inside --vault")
    vault_root = vault.expanduser().resolve(strict=True)
    if not vault_root.is_dir():
        raise ValueError("--vault must be an existing directory")
    target = (vault_root / output).resolve(strict=False)
    try:
        target.relative_to(vault_root)
    except ValueError as exc:
        raise ValueError("--output resolves outside --vault") from exc
    if target == vault_root:
        raise ValueError("--output must name a file below --vault")
    return target


def render(tasks: list[dict], board: str) -> str:
    groups: dict[str, list[dict]] = defaultdict(list)
    for task in tasks:
        groups[safe_text(task.get("status")) or "todo"].append(task)

    generated = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    board_value = safe_text(board) or "default"
    lines = [
        "---",
        "type: dashboard",
        "dashboard: hermes-kanban",
        "managed_by: obsidian-kanban-sync",
        f"hermes_board: {json.dumps(board_value, ensure_ascii=False)}",
        f"generated: {json.dumps(generated)}",
        "---",
        "",
        "# Kanban Hermes",
        "",
        "> [!info] Espelho somente leitura",
        "> Hermes Kanban é a fonte canônica. Este arquivo é regenerado; não edite cartões aqui. Use o painel do Hermes ou `hermes kanban` para alterar estado, comentário ou responsável.",
        "",
    ]
    statuses = STATUS_ORDER + [s for s in groups if s not in STATUS_ORDER and s != "archived"]
    for status in statuses:
        label = STATUS_LABELS.get(status, markdown_text(status.title()))
        lines.extend([f"## {label}", ""])
        cards = sorted(
            groups.get(status, []),
            key=lambda item: (-priority_value(item.get("priority")), safe_text(item.get("title")).lower()),
        )
        if not cards:
            lines.extend(["_Nenhum cartão._", ""])
            continue
        for task in cards:
            task_id = code_text(task.get("id") or task.get("task_id"))
            title = markdown_text(task.get("title")) or "Sem título"
            assignee = code_text(task.get("assignee"))
            priority = code_text(task.get("priority"))
            meta = []
            if assignee:
                meta.append(f"responsável: `{assignee}`")
            if priority and priority != "0":
                meta.append(f"prioridade: `{priority}`")
            suffix = " · " + " · ".join(meta) if meta else ""
            identifier = f" `{task_id}`" if task_id else ""
            lines.append(f"- **{title}**{identifier}{suffix}")
        lines.append("")
    if groups.get("archived"):
        lines.extend(["## Arquivadas", "", f"{len(groups['archived'])} cartão(ões) arquivado(s) — omitidos da visão principal.", ""])
    return "\n".join(lines).rstrip() + "\n"


def write_atomic(target: Path, content: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=target.parent, delete=False) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    try:
        os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", required=True, type=Path)
    parser.add_argument("--output", default=Path("Indexes/Kanban Hermes.md"), type=Path)
    parser.add_argument("--board", default="default")
    parser.add_argument("--hermes", default="hermes")
    args = parser.parse_args()
    target = resolve_output(args.vault, args.output)
    board = safe_text(args.board) or "default"
    tasks = fetch_tasks(args.hermes, None if board == "default" else board)
    write_atomic(target, render(tasks, board))
    print(json.dumps({"board": board, "tasks": len(tasks), "output": str(target)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
