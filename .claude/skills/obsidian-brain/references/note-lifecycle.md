# Note lifecycle

## Raw note
Required defaults: `type: fleeting`, `status: inbox`, `created`, `updated`, `topics: []`, `projects: []`.
Allowed states: `inbox`, `incubating`, `ready`, `processed`, `archived`.

`processed` requires a real `developed_into` wikilink. `archived` means no current processing is needed, not that the idea is false or worthless.

## Complete note
Use `type: evergreen`, `status: active`, `source_notes`, and `confidence: low|medium|high`.
Body sections: Idea central, Development, Evidence and sources, Relationships, Open questions.

## Transition rules
- Never delete or replace a raw note.
- Draft before create, split, or merge.
- Require approval before rename, move, merge, archive, or status transition.
- Preserve source voice and uncertainty.
