---
name: obsidian-brain:process
description: Full end-of-session processing — deep extraction, daily note update, run all learned rules, then suggest context compression after saving. Use when the user is wrapping up a working session, says "end session", "wrap up", "save and compact", or invokes /obsidian-brain:process directly. This is the most thorough sync; prefer obsidian-brain:quick-sync for lightweight mid-session checkpoints.
---

# Obsidian Brain — Process (full + offer compact)

End-of-session workflow. Save everything to the vault, then offer to compact the conversation for a fresh context.

## Step 1 — Load context

Read both files:
1. `~/.agents/obsidian-brain/config.md`
2. `~/.agents/obsidian-brain/brain-rules.md`


If missing, create from defaults in the skill's `references/defaults.md`.

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

For detailed extraction guidance, see the skill's `references/extraction.md`.

## Step 3 — Update the daily note

Determine today's date and current project (basename of working directory).

Follow the daily note format in the skill's `references/daily-note.md`:
- Create the daily note if it doesn't exist (use the template from config)
- Smart-append if it exists (no duplicate TODOs)
- Add session entry under `## Sessions`
- Merge TODOs into `## Tasks`
- Add observations under `## Notes`

Use **obsidian CLI** if Obsidian is open (`obsidian daily:append`), otherwise write directly to the filesystem at the path in `config.md`.

## Step 4 — Execute extra rules

For each rule in `~/.agents/obsidian-brain/brain-rules.md` under `## Learned Rules`, check if it applies to this session and execute it. Common patterns:
- Maintain per-project activity logs
- Create separate notes for architecture decisions
- Update reference notes for cited papers/links
- Track technical debt with tags

## Step 5 — Learn new rules

Scan the conversation for **meta-instructions** (anything about how the brain should behave). For each:
1. Open `~/.agents/obsidian-brain/brain-rules.md`
2. Append under `## Learned Rules` with today's date
3. Don't duplicate — refine existing rules instead
4. Confirm what was learned

See the skill's `references/learning.md` for details.

## Step 6 — Show summary

```
✅ Daily note updated: [[YYYY-MM-DD]]
📝 Session logged: HH:MM — project · descriptive title
📋 N TODOs added · N decisions logged
🧠 N new rules learned: "..."
📂 Files updated: <list>
```

## Step 7 — Suggest context compression (REQUIRED for process)

After the summary, suggest the user free up context. Just tell them the command — **never run it yourself**.

Pick the right command based on the current agent:

| Agent | Command |
|-------|---------|
| Gemini CLI / Antigravity | `/compress` |
| All others | start a new session |

Present this message verbatim, filling in `<command>`:

```
🧠 Session saved to your vault.

To free up context: <command>
```

That's it. One line. Do not ask "would you like me to…" — just show the command and let the user decide.
