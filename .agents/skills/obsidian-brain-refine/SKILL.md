---
name: obsidian-brain:refine
description: Refine raw notes into sourced evergreen notes.
version: 0.3.0
author: Obsidian Brain contributors, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Obsidian, Writing, Evergreen Notes, PKM]
    related_skills: []
---
# Obsidian Brain — Refine

Create a mature, sourced note from raw material while retaining provenance. Safe automation may create draft complete notes; approval is still required before promotion, merging, or changing a source lifecycle state.

## When to Use

- The user asks to polish, refine, complete, split, or consolidate a note.
- The user selects a candidate from the refinement queue.
- A scheduled review asks for automatic draft creation from ready candidates.
- Do not use for bulk inbox classification or more than the configured batch size.

## Prerequisites

Resolve the vault from the active profile configuration. Load `brain-rules.md`, `references/note-lifecycle.md`, and `references/safety-and-provenance.md`.

## Procedure

1. Resolve the requested source exactly. In automatic mode, select at most the configured batch size from raw notes explicitly marked `status: ready`; if none are marked ready, select substantial recent raw notes that contain a developed claim, explanation, decision, or recurring concept. Exclude credentials, private notes, templates, task-only lists, and fragments that cannot support a coherent note. Completion: every selected source has a recorded selection reason.
2. Read the complete source and any directly cited material. Separate claims, hypotheses, questions, tasks, references, and personal reflections. Completion: inferred content is labeled.
3. Search complete notes, source material, and project notes for overlap. Completion: potential merge targets are listed with evidence.
4. Choose one recommendation: create, merge, split, or incubate. Completion: explain why the alternative actions are weaker.
5. Write the new artifact under the configured complete-note draft folder (default `3 - Notas completas/_Rascunhos/`) using the evergreen template with `type: evergreen`, `status: draft`, `generated_by: obsidian-brain`, `source_notes`, confidence, evidence, relationships, and open questions. This write is allowed without approval because it is additive and leaves sources untouched. Completion: the draft is visible inside the complete-notes hierarchy and contains no unsupported citation or fabricated fact.
6. Before creating a file, search existing complete notes and drafts for the same source path. If a draft already represents that source, update it only when the source materially changed; never create a duplicate. Completion: each source maps to at most one automatic draft.
7. Present the draft path and a compact transformation summary. Do not update the source status or an existing active complete note without explicit approval. Completion: user can review a concrete artifact.
8. After approval, move or merge the draft into the active complete-notes folder, change it to `status: active`, then add `developed_into` and `status: processed` to the source. Preserve the raw body. Completion: source and destination link to each other.

## Pitfalls

- Stylistic polish must not erase uncertainty or personal voice.
- A long note is not necessarily several atomic notes.
- Never invent bibliographic metadata from a filename.
- Avoid converting aspirations into tasks unless the text states an action commitment.
- Automatic mode must skip rather than pad a batch with weak candidates.

## Verification

Read source and destination. Confirm provenance links in both directions, source body preservation, and a clear distinction between evidence and inference.
