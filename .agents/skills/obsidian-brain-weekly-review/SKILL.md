---
name: obsidian-brain:weekly-review
description: Prepare an evidence-backed Obsidian weekly review.
version: 0.3.0
author: Obsidian Brain contributors, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Obsidian, Tasks, Weekly Review, PKM]
    related_skills: []
---
# Obsidian Brain — Weekly Review

Prepare a review of commitments, completed work, inbox state, and active themes. Suggest priorities but leave commitments and archiving decisions to the user.

## When to Use

- The user requests a weekly review or planning reset.
- A scheduled job prepares a non-destructive weekly digest.

## Prerequisites

Resolve the vault and load `references/reflection.md`, `references/task-policy.md`, and `references/safety-and-provenance.md`. Determine current date with `terminal`.

## Procedure

1. Run the bundled report helper in read-only or report mode for the configured vault. Completion: task and note counts are available.
2. Read the configured Dataview task dashboard path. Use source checkboxes for analysis, but never copy them into the weekly report; the live dashboard remains the unified task surface. Completion: task categories point to the dashboard and any discussed item retains its source-note link.
3. Review raw notes in `inbox` or `ready`, isolated complete notes, unresolved questions, and active projects without recent updates. Completion: every listed item links to a source.
4. Summarize completed work separately from open commitments. Completion: done and open tasks are never mixed.
5. Suggest up to three priorities with rationale and identify uncertainty. Do not edit task status or due dates. Completion: priorities are proposals, not commitments.
6. Run triage and, when automatic drafts are enabled, create up to the configured batch size of sourced complete-note drafts from strong candidates. Completion: each candidate has a draft path or a documented skip reason.
7. Refresh `Sistema/Revisão semanal.md` and optionally create a dated snapshot in `Diário/Revisões semanais/`. Completion: generated date and coverage are explicit.

## Pitfalls

- A checked box is evidence of completion; conversational claims alone are not.
- Do not assign dates to undated tasks automatically.
- Exclude template examples and archived folders from task totals.

## Verification

Recompute all declared totals, verify source links, and confirm that no task checkbox or due date was modified.
