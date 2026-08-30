---
name: obsidian-brain:mvp
description: Turn a raw idea into a scoped, testable MVP plan.
version: 0.1.0
author: Obsidian Brain contributors, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
---
# Obsidian Brain — Idea to MVP

Convert one explicit idea into a small, falsifiable MVP without mutating the source note.

## When to use

- The user asks to turn an idea into an MVP, prototype, experiment, or validation plan.
- The user selects an item from `Indexes/Ideias.md`.
- Do not use vague fragments that do not identify a problem, audience, or observable outcome; keep those incubating.

## Procedure

1. Resolve and read the complete source idea. Extract only explicit problem, audience, proposed value, constraints, evidence, and open questions. Label every inference.
2. Search `1 - Notas brutas/`, `3 - Notas completas/`, and `Projects/` for overlap. Prefer linking an existing project over creating a duplicate.
3. Write `Projects/MVPs/<slug>/MVP.md` from the MVP template. Preserve a `source_notes` wikilink, `status: draft`, thematic tags, and a one-sentence falsifiable value hypothesis.
4. Define the smallest test: target user, one core workflow, explicit non-goals, success metric, stopping rule, risks, and evidence to collect. A feature list without a validation method is not an MVP.
5. Write `Projects/MVPs/<slug>/Backlog.md` with Tasks-compatible Markdown. Keep at most seven initial tasks; use dependencies and explicit due dates only when the source or user supplies them.
6. If Hermes Kanban is available, create cards only when the user asked to execute or track the MVP. Use idempotency keys derived from the source path and task slug. Leave cards unassigned unless the user selected a profile. Record returned task IDs in `MVP.md`.
7. Refresh `Indexes/Ideias.md`, `Indexes/Tags.md`, and the read-only `Indexes/Kanban Hermes.md` mirror. Do not copy task checkboxes into an additional report.
8. Present the created paths, assumptions, metric, and the single riskiest uncertainty. Promotion from draft to active remains an editorial decision.

## Verification

Confirm the source body is unchanged; every claim has a source or is labeled inference; the MVP has one core workflow, non-goals, metric, and stopping rule; no Kanban card was duplicated.
