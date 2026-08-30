---
name: obsidian-brain:graph
description: Explore the local Obsidian knowledge graph.
version: 0.2.0
author: Obsidian Brain contributors, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Obsidian, Knowledge Graph, Local Search, PKM]
    related_skills: []
---
# Obsidian Brain — Graph

Inspect wikilink edges and local vector-neighbor candidates without paid services. Wikilinks are explicit graph evidence; vector neighbors are suggestions, not asserted relations.

## When to Use

- The user asks what connects to a note or which ideas are nearby.
- The user asks for graph statistics or isolated concepts.

## Prerequisites

Resolve the database path and configured vault. Load `references/link-policy.md` and `references/messaging-knowledge-base.md`.

## Procedure

1. Ensure the local index exists and is current enough for the request. Rebuild when needed. Completion: generation time is known.
2. Run `scripts/knowledge_base.py --db <db> related "<note>" --limit 10` through `terminal`. Completion: explicit incoming/outgoing links and vector neighbors are returned separately.
3. Read source and candidate notes before explaining a relationship. Completion: semantic claims cite both endpoints.
4. Report explicit graph links first, then label local-vector neighbors as candidates with scores. Completion: similarity is never described as a proven relationship.
5. To modify notes, hand candidates to `obsidian-brain:connect`; do not write body links directly. Completion: exploration remains read-only.

## Verification

Check cited paths, distinguish graph edges from similarity, and verify any relationship explanation against both source notes.
