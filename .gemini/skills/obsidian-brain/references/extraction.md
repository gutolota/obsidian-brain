# Reference — Extracting from a conversation

Detailed guidance on what to pull from an agent conversation when running any obsidian-brain skill.

## Categories

### Summary
3-6 dense sentences describing what was done. Capture intent + outcome, not minutiae. Examples:
- ✓ "Implemented JWT auth middleware for v2 API routes. Decided on RS256 over HS256 for asymmetric verification. Wired role checks into the existing permission system."
- ✗ "We talked about auth. Then we wrote some code. Then we tested it."

### Technical decisions
Choices with **reasoning**, not just outcomes:
- ✓ "Use Postgres RLS instead of application-level filtering — simpler audit story, single source of truth"
- ✗ "Used Postgres RLS"

Format as bullets in a `> [!summary]` callout.

### Files touched
Group by action when many files:
```markdown
**Files:**
- Created: `src/middleware/auth.ts`, `src/types/jwt.ts`
- Edited: `src/routes/api.ts`, `src/config/permissions.yaml`
- Deleted: `src/legacy/auth-old.ts`
```

If only a few, inline format:
```markdown
**Files:** `src/middleware/auth.ts`, `src/routes/api.ts`
```

### TODOs / next steps
Capture concrete, actionable items. Add enough context to resume cold:
- ✓ `- [ ] Write integration tests for auth middleware (cover token expiry, role mismatch)`
- ✗ `- [ ] Tests`

Check existing daily note `## Tasks` before adding — don't duplicate.

### Learnings
Things worth remembering for next time:
- Gotchas discovered
- Bugs found and root causes
- Patterns that worked or didn't
- Performance observations

Format as bullets, group under `## Notes` in daily note if quick-sync, or in a dedicated callout for `process`.

### References
Anything cited or linked:
- URLs → `[title](url)` or `<url>` if no good title
- Papers → `[[Author-Year]]` if a reference note exists, or full citation
- Tools/libraries → wikilinked if there's a project note for them
- Documentation → URL with descriptive label

### Open questions
Unresolved items that aren't TODOs (because they need investigation, not action):
- "Is X behavior intentional or a bug?"
- "Should Y be configurable?"

Add as a `> [!question]` callout when relevant.

### Meta-instructions (CRITICAL)
**Always scan for these.** They become rules. See `learning.md`.

## What NOT to extract

- Greetings, small talk, off-topic banter
- The fact that you used a tool (the *result* matters, not the call)
- Restating what the user said back to them
- Conversational filler
- Failed attempts that got rolled back (unless the failure is a learning)

## Granularity by mode

| Mode | Summary | Decisions | Files | TODOs | Learnings | References | Open Q's |
|------|---------|-----------|-------|-------|-----------|------------|----------|
| quick-sync | 2-3 sent | only if material | always | always | optional | optional | skip |
| process | 4-6 sent | always | always | always | always | always | always |

When in doubt, prefer inclusion for `process` and exclusion for `quick-sync`.
