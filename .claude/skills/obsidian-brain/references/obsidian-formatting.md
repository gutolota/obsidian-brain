# Reference — Obsidian Flavored Markdown

Formatting rules for content written to the vault.

## Wikilinks

Internal references between notes. Obsidian auto-resolves these to existing notes or creates new ones.

```markdown
[[Note Name]]              ← link to "Note Name.md"
[[Note Name|display text]] ← link with custom display text
[[Note Name#Heading]]      ← link to a specific heading
[[Note Name#^block-id]]    ← link to a specific block
```

**Rules:**
- Use wikilinks for project names: `[[my-project]]`
- Use wikilinks for dates: `[[2026-05-06]]` (creates daily note links)
- Use wikilinks for any concept that has (or should have) a dedicated note
- Use external `[label](url)` for web URLs

## Properties (YAML frontmatter)

Top-of-file metadata between `---` markers:

```markdown
---
date: 2026-05-06
tags: [daily-note, project]
aliases: [Tuesday]
status: in-progress
---
```

Keys are always lowercase. Values can be:
- Strings: `title: "My Note"`
- Lists: `tags: [a, b, c]` or block style
- Dates: `date: 2026-05-06` (no quotes for ISO dates)
- Booleans: `published: true`

## Callouts

Highlighted blocks with semantic types:

```markdown
> [!note]
> Plain note callout

> [!summary] Decisions
> - Decision 1
> - Decision 2

> [!warning] Caution
> Something to watch out for

> [!tip]
> Helpful tip

> [!important]
> Don't miss this

> [!question] Open question
> Something unresolved

> [!example]
> Sample code or usage

> [!quote]
> "Cited content"
```

Types used by obsidian-brain:
- `summary` → for decisions and key takeaways
- `question` → for open questions
- `warning` → for gotchas, tech debt
- `tip` → for useful patterns discovered

You can collapse callouts by default with `[!type]-` (collapsed) or `[!type]+` (expanded).

## Tags

Inline `#tag` or in frontmatter `tags: [tag]`. Both forms are searchable.

```markdown
This session involved #refactoring and #performance work.

Hierarchical: #project/my-api #status/done
```

Use sparingly inline. Frontmatter tags are preferred for note-level categorization.

## Embeds

Pull content from another note:

```markdown
![[Note Name]]              ← embed entire note
![[Note Name#Heading]]      ← embed a section
![[image.png]]              ← embed image (must be in vault)
![[file.pdf]]               ← embed PDF
```

Use sparingly — embeds make the note dependent on other files.

## Checkboxes

Tasks:
```markdown
- [ ] Pending task
- [x] Completed task
- [/] In progress (some themes)
- [!] Important
- [?] Question
- [-] Cancelled
```

Standard tasks (`[ ]` and `[x]`) work everywhere. Custom states (`[/]`, etc.) work in some themes but not all. **Default to `[ ]` and `[x]` only** for portability.

## Block references

Reference a specific block (paragraph, list item, etc.) from another note:

```markdown
This is an important paragraph. ^my-block-id

(then in another note:)
See [[Source Note#^my-block-id]]
```

## Code blocks

Standard markdown:

````markdown
```python
def hello():
    print("world")
```
````

Obsidian renders syntax highlighting for most languages.

## Tables

Standard markdown tables:

```markdown
| Col 1 | Col 2 |
|-------|-------|
| a     | b     |
```

For complex layouts, use Bases (separate `.base` files) — see kepano's obsidian-bases skill.

## Best practices for obsidian-brain output

1. **Always wikilink dates** — enables daily note backlinks
2. **Always wikilink project names** — builds the project graph
3. **Use callouts for emphasis** — better than bold for structure
4. **Frontmatter for metadata** — avoids cluttering the body
5. **Standard checkboxes only** — `[ ]` and `[x]`, no fancy states
6. **Code blocks for paths** — single backticks for inline paths: `` `src/file.ts` ``
7. **External links** for URLs — `[label](url)`, not bare URLs
