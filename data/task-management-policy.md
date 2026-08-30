# Regra de gestão de tasks — preparação

> Artefato de preparação gerenciado pelo Obsidian Brain. Não altera notas-fonte automaticamente.

## Escopo e segurança

- Uma task só é válida quando há ação concreta, objeto identificável e contexto suficiente na nota-fonte.
- Não converter desejos vagos, exemplos, citações, obrigações de terceiros ou perguntas em tasks sem compromisso explícito do usuário.
- Preservar o texto original da task, a nota-fonte, datas do Tasks plugin, prioridade, recorrência e data de conclusão.
- Nunca marcar uma task como concluída sem checkbox já marcado na fonte ou aprovação explícita.

## Datas

- **Due-date explícita**: somente uma data declarada como prazo/entrega/vence até, ou uma data reconhecida pelo formato do Tasks plugin na task. Registrar como `due_date_explicit: YYYY-MM-DD`.
- **Data proposta**: data sugerida pelo agente, inferida de contexto ou necessária para planejamento. Registrar separadamente como `proposed_date: YYYY-MM-DD`; nunca apresentá-la como prazo.
- Se houver apenas data proposta, a task não deve ser tratada como vencida.
- Classificar como **atrasada** somente quando `due_date_explicit < data corrente` e a task estiver aberta. A data corrente deve ser obtida no momento da execução, não presumida.

## Arquivamento de concluídas

- Arquivar apenas tasks já concluídas na nota-fonte, sem modificar o corpo da nota-fonte sem aprovação editorial.
- Usar período configurável `completed_archive_after_days` (padrão recomendado: `30`). Uma task só entra na fila de arquivamento quando sua data de conclusão for anterior a `data corrente - completed_archive_after_days`.
- O destino deve ser separado por ano e mês, por exemplo `Sistema/Arquivo de tasks/YYYY/YYYY-MM.md` (ou a pasta equivalente definida na configuração).
- O arquivo deve preservar o texto original, link para a nota-fonte, data de conclusão e metadados relevantes. Duplicatas devem ser evitadas por identificador estável (fonte + texto + data de conclusão).
- A movimentação/remoção da task da nota-fonte exige aprovação explícita; sem aprovação, gerar somente um relatório/fila de arquivamento.

## Resultado esperado

O painel Dataview deve separar: abertas atrasadas, para hoje, próximas, sem prazo, todas as abertas e concluídas recentes. Relatórios interpretativos podem destacar tasks válidas ou ambíguas, prazos explícitos, datas propostas e itens elegíveis para arquivamento, mas não devem copiar o inventário inteiro nem criar checkboxes duplicados. Informar data de execução, configuração aplicada e links relativos aos artefatos.
