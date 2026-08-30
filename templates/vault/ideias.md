---
type: index
index: ideas
managed_by: dataview
---

# Ideias

> [!tip] Fluxo
> Capture livremente com `type: idea` ou tag `#idea`. Quando houver problema, público e resultado observável, use `/obsidian-brain:mvp` para criar um MVP em `Projects/MVPs/`.

## Por maturidade

```dataview
TABLE maturity AS "Maturidade", status AS "Estado", file.tags AS "Tags", file.mtime AS "Atualizado"
FROM "1 - Notas brutas"
WHERE type = "idea" OR contains(file.tags, "#idea") OR contains(file.tags, "#ideia")
SORT choice(maturity = "ready", 0, choice(maturity = "developing", 1, 2)) ASC, file.mtime DESC
```

## Ideias por tag

```dataview
TABLE rows.file.link AS "Ideias"
FROM "1 - Notas brutas"
WHERE type = "idea" OR contains(file.tags, "#idea") OR contains(file.tags, "#ideia")
FLATTEN file.tags AS tag
GROUP BY tag
SORT key ASC
```

## MVPs derivados

```dataview
TABLE status AS "Estado", source_notes AS "Origem", success_metric AS "Métrica", file.mtime AS "Atualizado"
FROM "Projects/MVPs"
WHERE type = "mvp"
SORT file.mtime DESC
```
