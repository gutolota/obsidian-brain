# Messaging knowledge base

## Surfaces
Hermes Gateway runs the same agent core, file tools, skills, and memory on Telegram and Discord. The Obsidian Brain therefore needs no paid SaaS connector: install the skills in the active Hermes profile, enable `skills`, `file`, and `terminal` for each platform, and keep the gateway running.

## Commands
- `obsidian-brain:query <question>`: read-only grounded retrieval.
- `obsidian-brain:capture <content>`: explicit opt-in capture to raw notes.
- `obsidian-brain:graph <note>`: explicit wikilinks plus local vector neighbors.
- `obsidian-brain:weekly-review`: non-destructive aggregate review.

## Privacy defaults
- DMs may query the full vault for an authorized owner.
- Shared channels must not expose `Diário/`, personal notes, credentials, private keys, or files marked private.
- Do not passively archive all group messages. Capture only explicit commands or approved channel workflows.
- Keep `group_sessions_per_user: true` unless a deliberately shared knowledge-room session is required.
- Discord should normally require mentions; Telegram groups should normally require mentions even when observation is enabled.

Credential detection is a best-effort defense-in-depth filter, not proof that every possible secret format was detected. Channel authorization and source-folder policy remain mandatory. In shared channels, retrieve only from paths allowed by `channel-policy.md`, inspect the cited source, redact sensitive values, and never reveal a raw index snippet merely because it was retrieved.

## Local retrieval architecture
The bundled helper uses SQLite FTS5, an explicit wikilink edge table, and 384-dimensional neural embeddings from `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` through FastEmbed/ONNX. It runs locally after the one-time model download, with no API, subscription, embedding bill, or external database. A deterministic hashed-vector backend remains available as a fallback.

Codex/ChatGPT subscription OAuth and Claude subscription OAuth are chat-generation entitlements, not general embedding API credentials. Do not assume they expose embedding endpoints. Nous Portal can proxy `/v1/embeddings` when the user's tier includes an embedding model, but local FastEmbed is the default zero-extra-cost backend.

## Grounding
Retrieval selects candidates. The agent must read candidate files before answering, cite vault paths or wikilinks, disclose index generation time when relevant, and say when evidence conflicts or is missing.
