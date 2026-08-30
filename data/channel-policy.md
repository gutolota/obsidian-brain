# Obsidian Brain — Channel Policy

## Direct messages

Authorized owner DMs may query the complete vault except secrets and credential-like files. Explicit captures are allowed.

## Shared Telegram and Discord channels

- Query defaults to `3 - Notas completas/`, `2 - Material fonte/`, `Projects/`, `Indexes/`, and public project notes.
- Never disclose `Diário/`, personal reflections, dreams, health notes, credentials, private keys, tokens, or files marked `visibility: private`.
- Never capture ordinary group chatter passively. Capture only an explicit command from an authorized user.
- Preserve per-user session isolation.
- If access scope is ambiguous, refuse the sensitive portion and ask the owner in a private channel.

## Commands

- `/obsidian-brain:query <question>` — grounded query with vault citations.
- `/obsidian-brain:capture <content>` — explicit capture to raw notes.
- `/obsidian-brain:graph <note>` — read-only graph and similarity exploration.
