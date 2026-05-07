# Reference — Learning new rules

How the brain detects user preferences and turns them into permanent rules.

## What counts as a meta-instruction

Any moment where the user expresses **how the brain should behave**, not what the current task should accomplish.

### Strong signals

- "always do X" / "from now on do X"
- "remember to X" / "don't forget to X"
- "I want you to X for every session"
- "add a section for X"
- "keep track of X in <file>"
- "skip X" / "don't bother with X"
- "when I do X, also do Y"

### Weak signals (use judgment)

- "this is useful, save it" → maybe save it, don't necessarily make a rule
- "I prefer X" → could be a rule, ask if unclear
- A repeated correction: if the user has corrected the same thing 2-3 times, that's a rule

### NOT meta-instructions

- Task-scoped requests: "save this conversation to my notes" is the action, not a rule
- Single-time preferences: "for this one, focus on X" applies only to this run

## Rephrasing into actionable rules

Take what the user said and rephrase it as an instruction the brain can execute consistently.

| User said | Rule text |
|-----------|-----------|
| "always log the libraries I install" | "Log every library installation (npm install, pip install, cargo add, etc.) in `Tooling/installs.md` with date and project context" |
| "I want a separate file for activities per project" | "Maintain `Projects/<project>/activity-log.md` with a chronological log of all sessions for that project" |
| "skip trivial debugging" | "Skip logging trivial debug sessions (typo fixes, import corrections, formatting) unless they reveal something structural" |
| "remember the papers I cite" | "For every paper or academic reference cited, create or update a note at `References/<first-author>-<year>.md` and wikilink it from the session entry" |

Rules should be:
- **Specific** — "log libraries" → "log npm/pip/cargo installs in `Tooling/installs.md`"
- **Actionable** — the brain knows what to do without further interpretation
- **Self-contained** — doesn't depend on context that may change

## Avoiding duplicates

Before adding a rule, scan existing `## Learned Rules` for similar entries. Use semantic similarity, not string matching.

Examples:
- New: "log all installed libraries" 
- Existing: "Log every npm install, pip install, etc."
- → DUPLICATE — don't add. Optionally refine the existing one.

- New: "create separate notes for architecture decisions"
- Existing: "Create a note in Projects/<project>/decisions/ for each major design choice"
- → DUPLICATE — same intent.

- New: "track tech debt with a tag"
- Existing: "Maintain activity logs per project"
- → DIFFERENT — both are valid, keep both.

## Refining vs adding

If the user contradicts or narrows an existing rule, **refine** instead of adding a contradicting rule.

Existing: `[2026-05-06] Skip logging trivial debug sessions`
User says: "Actually, log debug sessions if they reveal something structural"

Update to:
```markdown
- [2026-05-06] Skip logging trivial debug sessions
  (REFINED on 2026-05-22: log if the debug revealed something structural — typos and import fixes still skipped)
```

This preserves history while updating behavior.

## Confirming to the user

After adding/refining a rule, always confirm:

```
🧠 New rule learned:
   "<rule text>"
   
   Saved to ~/.claude/obsidian-brain/brain-rules.md
   Will apply to all future syncs.
```

Or for refinement:
```
🧠 Existing rule refined:
   Before: "<old rule>"
   After:  "<new phrasing>"
```

Brief, clear, no fluff.

## When in doubt — ask

If a meta-instruction is ambiguous, ask before saving:

> "I noticed you said '<X>'. Should I add this as a permanent rule?
> Suggested phrasing: '<Y>'  
> (yes / no / different phrasing)"

Better to ask than to clutter `brain-rules.md` with rules the user didn't actually want.

## Rules apply globally by default

Unless the rule explicitly mentions a specific project or context, it applies to **every** future sync across **all** projects. This is the default. Users who want project-scoped rules should phrase them that way.

Example of project-scoped: "When working in the `my-api` project, always update `Projects/my-api/api-changelog.md`"
Example of global: "Always log dependency installations in `Tooling/installs.md`"
