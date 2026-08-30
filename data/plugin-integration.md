# Obsidian plugin integration contract

Markdown files in the vault remain the source of truth. Plugins provide views, capture, formatting, and navigation; they must not require a second task database or duplicate source checkboxes.

## Daily notes and Calendar

- Core Daily Notes folder: `Diário`.
- Template: `Templates/Daily.md`.
- File format: `YYYY-MM-DD`.
- Calendar opens the same daily-note path and starts weeks on Monday.
- Daily notes use `## Sessions`, `## Tasks`, and `## Notes` so the agent skills and plugins share one structure.

## Tasks

- Global filter is empty: every Markdown checkbox is indexed; `#task` is not required.
- Canonical metadata: `🛫` start, `⏳` scheduled, `📅` due, `🔁` recurrence, `✅` completion.
- Automatic created, completion, and cancellation dates may be enabled.
- A due date is added only when explicitly committed. Proposed dates remain prose until approved.
- Tasks remain in their source notes, including `Diário/`.

## Dataview

- `Indexes/Tarefas.md` scans the whole vault, including `Diário/`, and excludes templates and generated system folders.
- Dataview renders live views; scripts must not copy task checkboxes into static reports.
- DataviewJS may be enabled for Metadata Menu; inline JavaScript stays disabled unless explicitly needed.

## Templates, Templater, and QuickAdd

- All templates live in `Templates/`.
- QuickAdd exposes `New note from template` and must keep online/AI providers disabled by default.
- Templater is available for manual expansion. Automatic execution on every new file remains off unless the user explicitly enables a reviewed folder mapping.
- Agent-created notes must still emit ordinary Markdown and valid frontmatter.

## Metadata Menu, Various Complements, and Linter

- Metadata Menu edits frontmatter and ignores generated/system folders.
- Various Complements suggests vault links and metadata while excluding generated/system folders.
- Linter uses conservative whitespace rules and ignores raw notes, source material, daily notes, templates, and generated/system folders.

## Verification

Create a temporary task in a daily note with a unique marker and a Tasks due date, verify that both Tasks and the Dataview dashboard can discover it, then remove the temporary line. Never claim plugin integration is working from configuration files alone.