# Obsidian Brain — Processing Rules

> [!important]
> This file is **alive**. The obsidian-brain skills read AND update this document.
> Edit manually whenever you want. New rules are learned automatically.

## Base Rules

These rules always apply when processing a session:

1. **Daily note entry**: every session generates an entry under `## Sessions` in today's daily note
2. **TODOs extracted**: any future action mentioned becomes `- [ ]` under `## Tasks`
3. **Wikilinks for projects**: project names are always linked as `[[ProjectName]]`
4. **Decisions recorded**: technical decisions go in a `> [!summary]` callout within the session entry
5. **Files listed**: created/edited files are listed with paths in inline code
6. **No duplicates**: before adding TODOs, check if they already exist in the daily note
7. **Raw notes are immutable sources**: never delete or replace their body; refine into a separate draft
8. **Editorial approval**: ask before rename, move, merge, archive, lifecycle state changes, or adding body links
9. **Evidence-backed reflection**: every trend or thematic claim cites source notes and labels inference
10. **Tasks stay contextual**: keep tasks in their source note and aggregate them live with Dataview; never copy task checkboxes into generated summaries
11. **Safe automatic refinement**: automation may create sourced `status: draft` notes under the configured complete-note draft folder, but it must not mark the source processed or promote the draft to active without approval

## Learned Rules

<!-- 
  This section grows automatically. Each rule has:
  - Date when it was learned
  - The rule text
  
  obsidian-brain skills never remove rules — they only refine or mark as inactive.
  To deactivate a rule, edit manually and append (INACTIVE) to the end.
-->

- **Task management safety and dates**: Validate that a task has a concrete action, identifiable object, and sufficient context before reporting it. Keep explicit due dates separate from proposed dates; only an open task with an explicit due date earlier than the execution date is overdue. Use configurable `completed_archive_after_days` before proposing archival. Never mark tasks complete without source evidence, and require approval before moving or removing completed tasks from source notes. See `task-management-policy.md` in the agent data directory.

_Additional learned rules may be added below._

## Monitored Projects

<!--
  Projects the brain knows about and their specific preferences.
  Added automatically the first time obsidian-brain runs in a project.
-->

_No projects registered yet._

## Formatting

- **Note language**: English
- **Style**: concise and technical — no fluff
- **Session heading**: `### HH:MM — project · short descriptive title`
- **Preferred callouts**: summary, tip, warning, important
- **Inline tags**: use when relevant, don't force them
