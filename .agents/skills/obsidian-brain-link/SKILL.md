---
name: obsidian-brain:link
description: Link the current workspace to a vault project folder. Run once per project to bind the working directory to a folder in the Obsidian vault. After linking, process and quick-sync will automatically write to that project's files. Use when the user says "link this project", "connect to vault", or invokes /obsidian-brain:link directly.
---

# Obsidian Brain — Link Workspace

Bind the current working directory to a vault project folder. Run once per project.

## Step 1 — Resolve inputs

- **Workspace**: current working directory (e.g. `/home/user/dev/my-app`)
- **Project folder argument**: taken from `$ARGUMENTS` (e.g. `Projects/my-app`)

If `$ARGUMENTS` is empty, suggest a default based on the workspace basename:
_"No folder specified. Suggested: `Projects/<workspace-name>`. Use this? (yes / or type a different path)"_

Wait for confirmation before proceeding.

## Step 2 — Register the link

Read `~/.agents/obsidian-brain/workspace-links.md`. If it doesn't exist, create it:

```markdown
# Obsidian Brain — Workspace Links

Maps working directories to vault project folders.
Managed automatically — edit manually if needed.

## Links

<!-- format: - /absolute/workspace/path → VaultFolder/project -->
```

Check for an existing entry for this workspace. If one exists, ask:
_"This workspace is already linked to `<existing>`. Replace it? (yes/no)"_

Add or update the entry:
```markdown
- `/home/user/dev/my-app` → `Projects/my-app`
```

## Step 3 — Bootstrap project files in the vault

Resolve the vault path from `~/.agents/obsidian-brain/config.md`.

In `<vault>/<project-folder>/`, create any missing files. **Never overwrite existing ones.**

### `context.md` (if missing)
```markdown
---
project: <workspace-name>
workspace: /absolute/workspace/path
tags: [project]
---

# <workspace-name> — Context

> Edit this file freely. It is loaded at the start of every session to give the agent background on this project. The more detail here, the better the agent understands what you're working on.

## Goal

<!-- What is this project trying to accomplish? -->

## Architecture

<!-- High-level structure: main components, key files, tech stack -->

## Conventions

<!-- Coding style, naming patterns, testing approach, anything non-obvious -->

## Current focus

<!-- What is actively being worked on right now? -->

## Key constraints

<!-- Performance requirements, compatibility targets, hard limits -->
```

### `activity-log.md` (if missing)
```markdown
---
project: <workspace-name>
tags: [project, activity-log]
---

# <workspace-name> — Activity Log

Chronological record of sessions. Managed automatically by obsidian-brain.

<!-- Entries are prepended by process and quick-sync — newest at the top -->
```

### `decisions.md` (if missing)
```markdown
---
project: <workspace-name>
tags: [project, decisions]
---

# <workspace-name> — Decisions

Technical decisions extracted from sessions. Managed automatically by obsidian-brain.

| Date | Decision | Reasoning |
|------|----------|-----------|
```

## Step 4 — Confirm

```
🔗 Workspace linked.

   /absolute/workspace/path
   → [[Projects/my-app]]

   Vault files ready:
   ✓ context.md       ← fill this in for best results
   ✓ activity-log.md  ← auto-maintained
   ✓ decisions.md     ← auto-maintained

Next: edit context.md with your project's goal and architecture,
then run /obsidian-brain:context at the start of any session.
```
