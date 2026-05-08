---
name: obsidian-brain:learn
description: Teach the brain a new rule without processing the current session. Use when the user explicitly wants to add a behavior rule, says "remember to always X", "from now on do Y", "add a rule:", or invokes /obsidian-brain:learn directly. The rule is stored in brain-rules.md and applied to all future syncs across all projects.
---

# Obsidian Brain — Learn

Teach the brain a new rule. Stored permanently in `brain-rules.md` and applied to every future sync.

## Step 1 — Get the rule text

Take the user's input from `$ARGUMENTS` and use it as the rule. Strip any leading prefix like:
- `learn:`
- `remember:`
- `add rule:`
- `rule:`

Whatever remains is the rule body.

If `$ARGUMENTS` is empty, ask the user: _"What rule should I learn? (e.g. 'always log the libraries I install in a separate file')"_ and wait for their reply.

## Step 2 — Validate and refine

Before adding the rule:

- **Check for duplicates**: read `~/.gemini/obsidian-brain/brain-rules.md` and compare with existing entries under `## Learned Rules`. If similar, propose refining the existing rule instead of adding a duplicate.

- **Make it actionable**: rephrase vague rules into actionable instructions if needed. Show the user the final phrasing before saving.
- **Confirm scope**: rules apply globally across all projects unless they explicitly mention a project. If the user says "for project X", make sure that's clear in the rule text.

Examples of good rule phrasing:
- ✓ "Maintain `Projects/<project>/activity-log.md` with chronological session entries"
- ✓ "Log every CLI tool I install with `npm install -g` or `pip install` in a `Tooling/installs.md` file"
- ✓ "Skip logging trivial debug sessions (typo fixes, import corrections)"
- ✗ "Be smarter about commits" (too vague — ask for specifics)

## Step 3 — Append to brain-rules.md

Open `~/.gemini/obsidian-brain/brain-rules.md` and add to the `## Learned Rules` section:

```markdown
- [YYYY-MM-DD] <rule text>
```

If the section is empty (still has the placeholder text), replace the placeholder with the first rule.

If refining an existing rule, update it in place and add a note:
```markdown
- [2026-05-06] Skip trivial debug sessions
  (REFINED on 2026-05-22: skip only typos and imports — log if structural)
```

## Step 4 — Confirm

```
🧠 Rule learned and saved.

  "<rule text>"

This rule will apply to all future /obsidian-brain runs.
Edit ~/.gemini/obsidian-brain/brain-rules.md to adjust manually.
```

**Do not process the current session** — that's the job of `obsidian-brain:process` or `obsidian-brain:quick-sync`. The user can chain commands if they want both.
