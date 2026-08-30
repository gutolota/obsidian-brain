# Obsidian Brain — Configuration

## Vault

- **Vault path**: `~/Documents/ObsidianVault`
- **Vault name** (for obsidian CLI): `MyVault`

## Folders

- **Raw Notes**: `1 - Notas brutas`
- **Source Material**: `2 - Material fonte`
- **Complete Notes**: `3 - Notas completas`
- **Daily Notes**: `Diário` (file format: `YYYY-MM-DD.md`)
- **Projects**: `Projects` (project notes go in `Projects/<project-name>/`)
- **Indexes**: `Indexes`
- **Task Dashboard**: `Indexes/Tarefas.md`
- **System Reports**: `Sistema`
- **Templates**: `Templates`

## Behavior

- **Writing mode**: `auto`
  - `cli` → always use `obsidian` CLI (requires Obsidian to be open)
  - `file` → always write directly to the filesystem
  - `auto` → try CLI first, fall back to filesystem
- **Create daily note if missing**: `yes`
- **Create project folder if missing**: `yes`
- **Confirm before writing**: `no` (writes session logs directly, shows summary after)
- **Confirm editorial changes**: `yes` (required for rename, move, merge, archive, status changes, and body links)
- **Preserve raw note bodies**: `yes`
- **Reflection window**: `30 days`
- **Weekly review day**: `Sunday`
- **Automatic complete-note drafts**: `yes`
- **Complete-note draft folder**: `3 - Notas completas/_Rascunhos`
- **Automatic refinement batch size**: `3`
- **Completed task archive after days**: `30`

## Local Knowledge Base

- **Database path**: `~/.hermes/obsidian-brain/knowledge.db`
- **Embedding backend**: `fastembed`
- **Embedding model**: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- **Embedding dimensions**: `384`
- **Hybrid retrieval**: `SQLite FTS5 + cosine similarity + wikilink graph`
- **Exclude generated reports**: `yes`
- **Exclude credential-like notes**: `yes`
- **Passive group capture**: `no`

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
- **Windows**: use `C:/Users/<username>/Documents/...` style paths (forward slashes work in most contexts)
