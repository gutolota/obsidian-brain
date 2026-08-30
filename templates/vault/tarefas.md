---
type: dashboard
dashboard: tasks
managed_by: dataview
---

# Tarefas

> [!info] Visão dinâmica
> As tarefas continuam nas notas de origem, inclusive em `Diário/`. O Dataview consulta toda a vault ao abrir esta nota; não há cópias nem rotina de atualização. O plugin Tasks deve usar filtro global vazio, portanto `#task` não é obrigatório.

> [!tip] Metadados reconhecidos
> Prazo `📅 YYYY-MM-DD` · agendamento `⏳ YYYY-MM-DD` · início `🛫 YYYY-MM-DD` · recorrência `🔁 ...` · conclusão automática `✅ YYYY-MM-DD`.

## Atrasadas

```dataview
TASK
FROM ""
WHERE !completed AND due AND due < date(today)
WHERE !startswith(file.path, "Templates/") AND !startswith(file.path, "Sistema/") AND !startswith(file.path, "analysis_outputs/")
SORT due ASC
GROUP BY file.link
```

## Para hoje

```dataview
TASK
FROM ""
WHERE !completed AND due = date(today)
WHERE !startswith(file.path, "Templates/") AND !startswith(file.path, "Sistema/") AND !startswith(file.path, "analysis_outputs/")
GROUP BY file.link
```

## Próximos 14 dias

```dataview
TASK
FROM ""
WHERE !completed AND due > date(today) AND due <= date(today) + dur(14 days)
WHERE !startswith(file.path, "Templates/") AND !startswith(file.path, "Sistema/") AND !startswith(file.path, "analysis_outputs/")
SORT due ASC
GROUP BY file.link
```

## Sem prazo explícito

```dataview
TASK
FROM ""
WHERE !completed AND !due
WHERE !startswith(file.path, "Templates/") AND !startswith(file.path, "Sistema/") AND !startswith(file.path, "analysis_outputs/")
SORT file.mtime DESC
GROUP BY file.link
```

## Todas as abertas

```dataview
TASK
FROM ""
WHERE !completed
WHERE !startswith(file.path, "Templates/") AND !startswith(file.path, "Sistema/") AND !startswith(file.path, "analysis_outputs/")
SORT due ASC
GROUP BY file.link
```

## Concluídas nos últimos 30 dias

```dataview
TASK
FROM ""
WHERE completed AND completion AND completion >= date(today) - dur(30 days)
WHERE !startswith(file.path, "Templates/") AND !startswith(file.path, "Sistema/") AND !startswith(file.path, "analysis_outputs/")
SORT completion DESC
GROUP BY file.link
```

## Concluídas sem data de conclusão

```dataview
TASK
FROM ""
WHERE completed AND !completion
WHERE !startswith(file.path, "Templates/") AND !startswith(file.path, "Sistema/") AND !startswith(file.path, "analysis_outputs/")
SORT file.mtime DESC
GROUP BY file.link
```