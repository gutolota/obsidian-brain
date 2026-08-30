---
name: obsidian-brain:agenda
description: Turn daily notes into tasks, deadline suggestions, and plans.
version: 0.2.0
author: Obsidian Brain contributors, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Obsidian, Daily Notes, Tasks, Planning]
    related_skills: []
---
# Obsidian Brain — Agenda

Process `Diário/` into one grounded view of open work, explicit deadlines, proposed dates, completed work, and context-aware suggestions. Never silently convert an inferred date into a real commitment.

## When to Use

- The user asks to process daily notes, collect tasks, organize deadlines, or suggest next actions.
- A scheduled daily planning job runs.
- Do not use to mark tasks complete or change due dates without approval.

## Prerequisites

Resolve the active Hermes home from `$HERMES_HOME` (default `~/.hermes`) and read `$HERMES_HOME/obsidian-brain/config.md` for the vault path before touching the vault. Resolve the current date with `terminal`. Then load `references/task-policy.md`, `references/daily-planning.md`, and `references/safety-and-provenance.md` from this skill directory.

## Procedure

1. Run the report helper to refresh deterministic task and note inventories. Completion: exact open/done totals are available.
2. Read daily notes from the last 14 days, plus older daily notes containing open tasks. Completion: every open task retains its source-note wikilink and original text.
3. Separate dates into: explicit Tasks-plugin dates, explicit natural-language deadlines, and inferred suggestions. Completion: no inferred date is labeled as a deadline.
4. Group open work as overdue, today, next seven days, later, undated, waiting, and someday. Completion: each item appears once.
5. Read nearby context around tasks and recent reflections. Suggest up to five next actions, schedule adjustments, or clarifying questions. Completion: each suggestion cites the note that motivated it.
6. Write `Sistema/Agenda e prazos.md` with sections for tasks, explicit deadlines, proposed dates pending approval, completed work, and suggestions. Do not edit source checkboxes or dates. Completion: the generated file is a single review surface.
7. If the user approves a proposed date or task rewrite, patch the exact source line and preserve all Tasks-plugin metadata. Completion: only approved source lines change.

## Date Rules

- Parse explicit ISO dates and Tasks-plugin markers as commitments already present in the source.
- Resolve relative expressions such as “amanhã” or “sexta” against the daily note date, not the automation run date.
- If an expression is ambiguous, add it under `Datas a confirmar` rather than choosing silently.
- A meeting date mentioned in prose is not automatically a task due date.

## Messaging

Telegram and Discord may request `/obsidian-brain:agenda`. In shared channels, do not expose personal daily-note content; provide only a high-level count unless the channel policy explicitly allows details.

## Verification

Recompute declared totals, verify every date against its source line and daily-note date, confirm all suggestions are labeled, and confirm no source task was modified without approval.
