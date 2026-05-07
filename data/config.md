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

```markdown
---
date: {{date}}
tags: [daily-note]
aliases: [{{day_of_week}}]
---

# {{date}} — {{day_of_week}}

## Sessions

## Tasks

## Notes
```

## Notes

- Edit this file freely — the obsidian-brain skills only read it, never modify `config.md`
- Paths with `~` are expanded automatically
- The "Vault name" field is only used by the obsidian CLI
