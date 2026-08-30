---
name: obsidian-brain:triage
description: Triage raw Obsidian notes without destroying sources.
version: 0.2.0
author: Obsidian Brain contributors, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Obsidian, Notes, Triage, PKM]
    related_skills: []
---
# Obsidian Brain — Triage

Turn an unstructured inbox into a reviewable queue. Preserve every source note and distinguish explicit content from agent inference.

## When to Use

- The user asks to organize, triage, classify, or clean raw notes.
- The user asks what should be refined next.
- Do not use for rewriting a selected note; use `obsidian-brain:refine`.

## Prerequisites

Read the configured vault path and folders from the active profile data directory. For Hermes this is `$HERMES_HOME/obsidian-brain/config.md`; resolve `$HERMES_HOME` before using file tools. Load `brain-rules.md`, `references/note-lifecycle.md`, and `references/safety-and-provenance.md`.

## Procedure

1. Use `search_files` to enumerate Markdown files in the raw-notes folder. Respect an explicit note or count limit; otherwise process at most 20 newest unprocessed notes. Completion: every candidate path is accounted for.
2. Read each candidate with `read_file`. Extract explicit tasks, questions, references, projects, and topics. Completion: each extraction can be cited to source text.
3. Recommend one state: `incubating`, `ready`, `processed`, or `archived`. Never mark `processed` without an existing destination note. Completion: every state has a one-sentence reason.
4. Search the vault by distinctive title terms and concepts. Suggest no more than five links per note and explain each relationship. Completion: every suggested target exists.
5. Write or refresh `Sistema/Sugestões de triagem.md` as a review queue. Do not rename, move, archive, or rewrite source notes automatically. Completion: the report links every examined source.
6. If the user explicitly approves specific metadata edits, use `patch` only on those notes and preserve body text byte-for-byte. Completion: each approved note has the requested metadata and unchanged body.

## Output Contract

For each note report: current link, proposed title, proposed status, explicit tasks, topics, project, link candidates, uncertainties, and recommended next action.

## Pitfalls

- A checkbox in quoted source material may not be the user's task.
- Similar vocabulary is not sufficient evidence for a link.
- Missing frontmatter does not mean a note is low quality.
- Never process the entire historical vault in one unreviewed batch.

## Verification

Re-read the generated queue. Confirm that every wikilink target exists, no source note was removed, and any applied metadata change was explicitly approved.
