---
name: obsidian-brain:quick-sync
description: Lightweight mid-session checkpoint — extract recent activity, append to today's daily note, apply learned rules. Faster and lighter than obsidian-brain:process. Use when the user wants to save progress without ending the session, says "checkpoint", "save progress", "quick save", or invokes /obsidian-brain:quick-sync directly. Does NOT suggest compression — use obsidian-brain:process for end-of-session wrap-up.
---

# Obsidian Brain — Quick Sync

Lightweight checkpoint for mid-session progress. Saves what matters, doesn't interrupt flow, doesn't offer to compact.

## Step 1 — Load context

Read:
1. `~/.gemini/obsidian-brain/config.md`
2. `~/.gemini/obsidian-brain/brain-rules.md`


If missing, create from defaults in the skill's `references/defaults.md`.

## Step 2 — Light extraction

Focus on what's **new** since the last sync (or since session start). Extract:

- **Summary** (2-3 concise sentences)
- **Files touched** in this segment
- **TODOs** mentioned recently
- **Key decisions** (only if material)
- **Meta-instructions** (always check — these become rules)

Skip exhaustive references and learnings — those belong to `process`.

For details, see the skill's `references/extraction.md`.

## Step 3 — Append to daily note

Follow the format in the skill's `references/daily-note.md`:
- Add a new session entry under `## Sessions`
- Merge new TODOs into `## Tasks` (no duplicates)

Use shorter session entries than `process` — quick-sync favors brevity:
```markdown
### HH:MM — <project> · <short title>
<2-3 sentence summary>

**Files:** `path1.ext`, `path2.ext`
```

Skip the decisions callout unless decisions are significant. Skip references unless they're crucial.

## Step 4 — Apply learned rules

Run only the rules that fit a checkpoint context. Skip rules that imply heavy reflection (e.g., "create separate decision notes" → those usually wait for `process`).

Use judgment: if a rule says "always log papers I cite" and a paper was cited, do it. If it says "create architecture decision notes for major decisions" and nothing major happened, skip.

## Step 5 — Learn new rules

Same as `process` — scan for meta-instructions and append to `~/.gemini/obsidian-brain/brain-rules.md` if found. See the skill's `references/learning.md`.

## Step 6 — Brief confirmation

```
✓ Quick-sync done — [[YYYY-MM-DD]] updated
  📝 1 session entry · 📋 N TODOs added
```

Keep it short. The user is still working — don't interrupt with a long summary.

**Do not suggest compression** — that's for `obsidian-brain:process`.
