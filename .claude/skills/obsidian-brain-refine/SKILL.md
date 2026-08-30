---
name: obsidian-brain:refine
description: Refine raw notes into sourced evergreen notes.
version: 0.2.0
author: Obsidian Brain contributors, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Obsidian, Writing, Evergreen Notes, PKM]
    related_skills: []
---
# Obsidian Brain — Refine

Create a mature, sourced note from raw material while retaining provenance. Draft first and require approval before changing lifecycle state or merging into an existing note.

## When to Use

- The user asks to polish, refine, complete, split, or consolidate a note.
- The user selects a candidate from the refinement queue.
- Do not use for bulk inbox classification.

## Prerequisites

Resolve the vault from the active profile configuration. Load `brain-rules.md`, `references/note-lifecycle.md`, and `references/safety-and-provenance.md`.

## Procedure

1. Resolve the requested source note exactly; if ambiguous, show matching paths rather than guessing. Completion: one source path is selected.
2. Read the complete source and any directly cited material. Separate claims, hypotheses, questions, tasks, references, and personal reflections. Completion: inferred content is labeled.
3. Search complete notes, source material, and project notes for overlap. Completion: potential merge targets are listed with evidence.
4. Choose one recommendation: create, merge, split, or incubate. Completion: explain why the alternative actions are weaker.
5. Draft under `Sistema/Rascunhos de lapidação/` using the evergreen template. Include `source_notes`, confidence, evidence, relationships, and open questions. Completion: no unsupported citation or fabricated fact appears.
6. Present the draft path and a compact transformation summary. Do not update the source status or an existing complete note without explicit approval. Completion: user can review a concrete artifact.
7. After approval, move or merge the draft into the complete-notes folder, then add `developed_into` and `status: processed` to the source. Preserve the raw body. Completion: source and destination link to each other.

## Pitfalls

- Stylistic polish must not erase uncertainty or personal voice.
- A long note is not necessarily several atomic notes.
- Never invent bibliographic metadata from a filename.
- Avoid converting aspirations into tasks unless the text states an action commitment.

## Verification

Read source and destination. Confirm provenance links in both directions, source body preservation, and a clear distinction between evidence and inference.
