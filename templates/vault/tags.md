---
type: index
index: tags
managed_by: dataview
---

# Tags e temas

> [!info] Índice vivo
> Este índice organiza notas por tags sem mover arquivos. `Sistema/` contém bastidores operacionais e não participa desta navegação.

## Tags mais usadas

```dataview
TABLE WITHOUT ID tag AS "Tag", length(rows) AS "Notas"
FLATTEN file.tags AS tag
WHERE !startswith(file.path, "Sistema/") AND !startswith(file.path, "Templates/") AND !startswith(file.path, "analysis_outputs/")
GROUP BY tag
SORT length(rows) DESC
```

## Notas recentes por tags

```dataview
TABLE file.tags AS "Tags", type AS "Tipo", status AS "Estado", file.mtime AS "Atualizado"
FROM ""
WHERE length(file.tags) > 0
  AND !startswith(file.path, "Sistema/")
  AND !startswith(file.path, "Templates/")
  AND !startswith(file.path, "analysis_outputs/")
SORT file.mtime DESC
LIMIT 100
```
