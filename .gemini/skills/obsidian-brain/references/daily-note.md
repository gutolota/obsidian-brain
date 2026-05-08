# Reference — Daily Note format

Detailed guidance on creating and updating Obsidian daily notes.

## Path resolution

From `config.md`:
- Vault path → e.g., `~/Documents/ObsidianVault`
- Daily Notes folder → e.g., `Journal`
- File format → `YYYY-MM-DD.md`

Full path: `<vault>/<daily-notes-folder>/<YYYY-MM-DD>.md`

Always expand `~` to `$HOME`.

## Creating a new daily note

If the file doesn't exist, create with this template (English, generic):

```markdown
---
date: YYYY-MM-DD
tags: [daily-note]
aliases: [<weekday name>]
---

# YYYY-MM-DD — <Weekday>

## Sessions

## Tasks

## Notes
```

Weekday names: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.

The user can override the template via `config.md` — check there first.

## Smart append (file already exists)

Read the file, then add content **without breaking existing structure**.

### Adding a session entry

Look for `## Sessions`:
- If found → append the new entry below the last existing session
- If not found → add the heading first, then the entry

### Adding TODOs

Look for `## Tasks`:
- If found → for each new TODO, check if a similar one already exists (fuzzy match by intent, not exact text). Skip duplicates.
- If not found → add the heading and the new TODOs

Examples of duplicates to detect:
- "Write tests for auth" ≈ "Add integration tests for auth middleware" → skip
- "Fix bug in parser" ≈ "Resolve parser issue with nested quotes" → skip  
- "Document API" ≈ "Update README with deployment steps" → these are DIFFERENT, keep both

When unsure, prefer keeping (better to have a duplicate the user removes than to silently drop a TODO).

### Adding notes

Under `## Notes`, append free-form observations. No deduplication needed for notes.

## Session entry format

### For `process` (full)

```markdown
### HH:MM — <project> · <descriptive title>
<2-4 sentence summary capturing what was done and why>

> [!summary] Decisions
> - Decision 1 with reasoning
> - Decision 2 with reasoning

**Files:** `path/to/file1.ext`, `path/to/file2.ext`

**References:** [[Note]], [Title](url)

> [!question] Open
> - Unresolved question 1
> - Unresolved question 2
```

Omit empty sections. If no decisions, skip the callout. If no references, skip the line.

### For `quick-sync` (light)

```markdown
### HH:MM — <project> · <short title>
<2-3 sentence summary>

**Files:** `path1.ext`, `path2.ext`
```

Short. No callouts unless decisions are significant.

## Project naming

Project name = basename of the working directory. If working in `~/code/my-app`, project is `my-app`.

Always wikilink: `[[my-app]]`. This creates an automatic backlink network in Obsidian.

## Time formatting

Use 24-hour format: `HH:MM` (e.g., `14:30`, not `2:30 PM`).

## Multiple sessions same day

Each invocation of `process` or `quick-sync` adds a new entry under `## Sessions`. Order chronologically (latest at the bottom). Time prefix makes the order clear regardless of how the file was edited.

## Writing mode

From `config.md`:
- **cli**: Use `obsidian daily:read` and `obsidian daily:append content="..."`. Requires Obsidian to be open.
- **file**: Read/write the file directly via standard tools.
- **auto**: Try CLI first (`obsidian --version` to test), fall back to file mode.

When using CLI mode, the multi-line content must be properly escaped or written to a temp file first then piped.

When using file mode, always read-then-write — never blind-overwrite.
