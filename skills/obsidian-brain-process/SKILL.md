---
name: obsidian-brain:process
description: Full end-of-session processing — deep extraction, daily note update, run all learned rules, then offer to /compact the conversation. Use when the user is wrapping up a working session, says "end session", "wrap up", "save and compact", or invokes /obsidian-brain:process directly. This is the most thorough sync; prefer obsidian-brain:quick-sync for lightweight mid-session checkpoints.
---

# Obsidian Brain — Process (full + offer compact)

End-of-session workflow. Save everything to the vault, then offer to compact the conversation for a fresh context.

## Step 1 — Load context

Read both files:
1. `~/.claude/obsidian-brain/config.md`
2. `~/.claude/obsidian-brain/brain-rules.md`

If missing, create from defaults in `~/.claude/skills/obsidian-brain/references/defaults.md`.

## Step 2 — Deep extraction

Scan the **entire** conversation. Extract more thoroughly than quick-sync:

- **Summary** (4-6 dense sentences — capture the arc of the session)
- **Technical decisions** (with reasoning, not just the choice)
- **Files touched** (created / edited / deleted, with paths)
- **TODOs / next steps** (concrete actions with enough context to resume later)
- **Learnings** (insights, gotchas, debugging discoveries)
- **References** (links, papers, tools, libraries mentioned)
- **Open questions** (unresolved issues worth flagging)
- **Meta-instructions** (anything about how the brain should work)

Apply ALL rules from `brain-rules.md` for additional extraction.

For detailed extraction guidance, see `~/.claude/skills/obsidian-brain/references/extraction.md`.

## Step 3 — Update the daily note

Determine today's date and current project (basename of working directory).

Follow the daily note format in `~/.claude/skills/obsidian-brain/references/daily-note.md`:
- Create the daily note if it doesn't exist (use the template from config)
- Smart-append if it exists (no duplicate TODOs)
- Add session entry under `## Sessions`
- Merge TODOs into `## Tasks`
- Add observations under `## Notes`

Use **obsidian CLI** if Obsidian is open (`obsidian daily:append`), otherwise write directly to the filesystem at the path in `config.md`.

## Step 4 — Execute extra rules

For each rule in `brain-rules.md` under `## Learned Rules`, check if it applies to this session and execute it. Common patterns:
- Maintain per-project activity logs
- Create separate notes for architecture decisions
- Update reference notes for cited papers/links
- Track technical debt with tags

## Step 5 — Learn new rules

Scan the conversation for **meta-instructions** (anything about how the brain should behave). For each:
1. Open `~/.claude/obsidian-brain/brain-rules.md`
2. Append under `## Learned Rules` with today's date
3. Don't duplicate — refine existing rules instead
4. Confirm what was learned

See `~/.claude/skills/obsidian-brain/references/learning.md` for details.

## Step 6 — Show summary

```
✅ Daily note updated: [[YYYY-MM-DD]]
📝 Session logged: HH:MM — project · descriptive title
📋 N TODOs added · N decisions logged
🧠 N new rules learned: "..."
📂 Files updated: <list>
```

## Step 7 — Offer /compact (REQUIRED for process)

After the summary, present this message verbatim:

```
🧠 Session processed and saved to your vault.

Would you like me to run /compact on this session?
This summarizes the conversation so far, freeing up context window space
while preserving key information. Useful for long sessions or before
starting a new task.

→ Reply "yes" or "go ahead" to compact, or just keep working.
```

**Do not run `/compact` without explicit user confirmation.** Wait for their reply. If they say yes, run `/compact`. Otherwise, continue normally.
