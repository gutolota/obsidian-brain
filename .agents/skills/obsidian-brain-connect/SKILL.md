---
name: obsidian-brain:connect
description: Find and justify semantic links between vault notes.
version: 0.2.0
author: Obsidian Brain contributors, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Obsidian, Wikilinks, Knowledge Graph, PKM]
    related_skills: []
---
# Obsidian Brain — Connect

Find meaningful relationships between notes. Prefer a few explained links over a dense graph of weak associations.

## When to Use

- The user asks to connect ideas, find related notes, or identify isolated notes.
- A refinement workflow needs relationship candidates.

## Prerequisites

Resolve the vault and load `references/link-policy.md` plus `references/safety-and-provenance.md`.

## Procedure

1. Read the selected note or bounded folder set. Completion: all candidate source paths are listed.
2. Extract concepts, claims, named projects, questions, and cited works. Completion: terms come from the source rather than filename alone.
3. Use `search_files` to retrieve candidate notes. Read each candidate before judging it. Completion: every recommended target was inspected.
4. Classify each strong relation as `supports`, `contradicts`, `extends`, `example_of`, `depends_on`, or `related`. Completion: each link has a one-sentence justification and confidence.
5. Write suggestions to `Sistema/Sugestões de links.md`. Apply links to note bodies only after explicit approval. Completion: report contains at most five high-value links per source note.

## Pitfalls

- Shared tags or keywords alone do not establish a semantic relationship.
- Do not create links to nonexistent titles unless clearly marked as a missing-note proposal.
- Contradiction claims require reading both notes.

## Verification

Confirm every accepted wikilink resolves to an existing note and every relationship is supported by text from both notes.
