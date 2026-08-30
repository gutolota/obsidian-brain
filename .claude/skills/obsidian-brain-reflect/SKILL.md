---
name: obsidian-brain:reflect
description: Track recurring ideas and changes across the vault.
version: 0.2.0
author: Obsidian Brain contributors, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Obsidian, Reflection, Trends, PKM]
    related_skills: []
---
# Obsidian Brain — Reflect

Produce an evidence-backed view of recurring themes, emerging questions, and shifts in attention. Frequency is a signal, not a diagnosis of interest or importance.

## When to Use

- The user asks what they have been thinking about.
- The user asks for a monthly reflection or thematic trend report.

## Prerequisites

Resolve the vault and load `references/reflection.md` plus `references/safety-and-provenance.md`. Determine current date with `terminal`; never infer it.

## Procedure

1. Use the configured window, default 30 days, and a preceding comparison window of equal length. Completion: exact date boundaries are recorded.
2. Enumerate notes modified or dated in each window and read a representative evidence set. Completion: report records coverage and exclusions.
3. Identify recurring topics, new topics, repeated questions, changed hypotheses, decisions, and raw-to-complete transitions. Completion: every claim cites supporting wikilinks.
4. Separate deterministic counts from semantic interpretations. Mark interpretations as hypotheses when evidence is limited. Completion: no frequency claim lacks a computed count.
5. Write a dated snapshot under `Diário/Reflexões/` and refresh `Sistema/Radar de pensamentos.md`. Completion: both documents state window and evidence links.

## Pitfalls

- File modification time can reflect syncing or formatting, not renewed interest.
- Silence does not prove abandonment.
- Repeated boilerplate and templates must not count as themes.

## Verification

Recompute displayed totals using the report helper, check sampled source notes, and ensure every interpretive statement is labeled and cited.
