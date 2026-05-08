# Reference — Defaults

Default content for `config.md` and `brain-rules.md` when bootstrapping the brain.

## Default config.md

Write this to `~/.agents/obsidian-brain/config.md` if it doesn't exist:

```markdown
# Obsidian Brain — Configuration

## Vault

- **Vault path**: `~/Documents/ObsidianVault`
- **Vault name** (for obsidian CLI): `MyVault`

## Folders

- **Daily Notes**: `Journal` (file format: `YYYY-MM-DD.md`)
- **Projects**: `Projects` (project notes go in `Projects/<project-name>/`)
- **Templates**: `Templates`

## Behavior

- **Writing mode**: `auto`
  - `cli` → always use `obsidian` CLI (requires Obsidian to be open)
  - `file` → always write directly to the filesystem
  - `auto` → try CLI first, fall back to filesystem
- **Create daily note if missing**: `yes`
- **Create project folder if missing**: `yes`
- **Confirm before writing**: `no` (writes directly, shows summary after)

## Daily Note Template

Used when creating a new daily note:

\`\`\`markdown
---
date: {{date}}
tags: [daily-note]
aliases: [{{day_of_week}}]
---

# {{date}} — {{day_of_week}}

## Sessions

## Tasks

## Notes
\`\`\`

## Notes

- Edit this file freely — `/obsidian-brain` only reads it, never modifies `config.md`
- Paths with `~` are expanded automatically
- The "Vault name" field is only used by the obsidian CLI
```

After creating, **inform the user**: _"Created default config at `~/.agents/obsidian-brain/config.md`. Please edit it to set your real vault path before running again."_

## Default brain-rules.md

Write this to `~/.agents/obsidian-brain/brain-rules.md` if it doesn't exist:

```markdown
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

## Learned Rules

<!-- 
  This section grows automatically. Each rule has:
  - Date when it was learned
  - The rule text
  
  obsidian-brain skills never remove rules — they only refine or mark as inactive.
  To deactivate a rule, edit manually and append (INACTIVE) to the end.
-->

_No rules learned yet. Use `/obsidian-brain:learn` or give instructions during sessions._

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
```

## When to bootstrap

- Bootstrap **config.md** only when missing — never overwrite
- Bootstrap **brain-rules.md** only when missing — never overwrite
- Bootstrapping happens transparently when any obsidian-brain skill needs the file

## After bootstrap

After creating defaults for the first time, the skill should:
1. Continue with the user's original request (don't make them re-run)
2. Use sensible defaults that work even if `config.md` still has the placeholder vault path (e.g., warn but don't fail)
3. Mention briefly that defaults were created so the user knows to customize them
