---
name: obsidian-brain:context
description: Load vault context for the current workspace. Reads context.md, decisions.md, and recent activity-log entries from the linked vault project folder and surfaces them as working memory for the session. Use at the start of a session, when the user says "load context", "what do we know about this project", or invokes /obsidian-brain:context directly.
---

# Obsidian Brain — Load Context

Load saved knowledge about the current project from the vault into the session.

## Step 1 — Check for a workspace link

Read `~/.claude/obsidian-brain/workspace-links.md` and look for an entry matching the current working directory.

If no link exists:
_"This workspace isn't linked to a vault project yet. Run `/obsidian-brain:link <Projects/folder>` to set one up."_
Stop here.

## Step 2 — Resolve vault paths

From `~/.claude/obsidian-brain/config.md`, get the vault path.

Construct paths for:
- `<vault>/<project-folder>/context.md`
- `<vault>/<project-folder>/decisions.md`
- `<vault>/<project-folder>/activity-log.md`

## Step 3 — Load files

Read each file that exists. For `activity-log.md`, load only the **5 most recent entries** (newest at top — stop after the 5th `###` heading).

If `context.md` is missing or has only the placeholder template content, note:
_"context.md hasn't been filled in yet — consider adding your project's goal and architecture for better results."_

## Step 4 — Surface as working memory

Present a structured summary the agent can reference throughout the session:

```
🧠 Project context loaded: [[<project-folder>]]
─────────────────────────────────────────────

📋 Goal
<content from context.md ## Goal>

🏗️ Architecture
<content from context.md ## Architecture>

🎯 Current focus
<content from context.md ## Current focus>

⚖️ Recent decisions
<last 3 rows from decisions.md table>

📅 Last session
<most recent entry from activity-log.md>

─────────────────────────────────────────────
Context is active. process and quick-sync will update project files automatically.
```

Omit sections that are empty or have only placeholder text.

## Step 5 — Stay active

The loaded context is now available for the rest of the session. When the user asks questions about the project, architecture, or past decisions — reference this context before answering.
