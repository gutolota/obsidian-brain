---
name: obsidian-brain:status
description: Show current Obsidian Brain configuration, learned rules, and monitored projects. Use when the user wants to inspect the brain's state, says "show config", "what rules do I have", "brain status", or invokes /obsidian-brain:status directly. Read-only — does not modify any files.
---

# Obsidian Brain — Status

Show the user a snapshot of the brain's current state. Read-only.

## Step 1 — Read state files

Read:
- `~/.claude/obsidian-brain/config.md`
- `~/.claude/obsidian-brain/brain-rules.md`

If either is missing, tell the user: _"Brain not initialized yet. Run `/obsidian-brain` once to create defaults, or run the setup script."_

## Step 2 — Format the report

Present a clean, scannable summary:

```
🧠 Obsidian Brain — Status
─────────────────────────────────────

📁 Vault
   Path: <vault path from config>
   Daily Notes: <folder>
   Projects: <folder>

⚙️  Behavior
   Writing mode: <cli | file | auto>
   Auto-create daily note: <yes/no>

📋 Base Rules: <count> active

🧠 Learned Rules: <count>
   Most recent:
   • [<date>] <rule text>
   • [<date>] <rule text>
   • [<date>] <rule text>
   (use /obsidian-brain:rules to see all)

📂 Monitored Projects: <count>
   • <project name> — <folder>
   • <project name> — <folder>

📄 Files
   Config:  ~/.claude/obsidian-brain/config.md
   Rules:   ~/.claude/obsidian-brain/brain-rules.md
```

## Step 3 — No writes

Don't modify anything. This is informational only.

If the user wants to change something, point them at the files:
- _"Edit `~/.claude/obsidian-brain/config.md` to change vault path or behavior."_
- _"Edit `~/.claude/obsidian-brain/brain-rules.md` to adjust rules manually, or use `/obsidian-brain:learn` to add new ones."_
