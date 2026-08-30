# Obsidian Brain — desenho de referência

## 1. Objetivo

Manter a captura livre e caótica em `1 - Notas brutas/`, sem exigir organização durante o pensamento, e construir uma camada assistida que:

1. reúna tarefas abertas e concluídas;
2. transforme notas brutas em notas completas sem apagar a fonte;
3. proponha links entre ideias com evidência;
4. acompanhe temas recorrentes, perguntas e mudanças de direção;
5. mantenha toda decisão editorial revisável pelo usuário.

Vault alvo: o caminho definido em `data/config.md` e copiado para o diretório de dados do agente durante a instalação.

## 2. Princípios

- **Captura sem atrito:** escrever primeiro, classificar depois.
- **Fonte preservada:** uma nota bruta nunca é sobrescrita nem apagada automaticamente.
- **Automação reversível:** lapidações criam rascunhos ou atualizações rastreáveis.
- **Links semânticos, não decorativos:** só criar links quando houver relação explicável.
- **Tarefas vivem nas notas de contexto:** dashboards apenas agregam, sem duplicar tarefas.
- **Poucas propriedades estáveis:** evitar uma taxonomia grande antes de ela ser necessária.
- **Separar fatos de inferências:** toda síntese automática deve indicar o que veio da fonte e o que foi inferido.

## 3. Camadas da vault

### 3.1 Captura

- `1 - Notas brutas/`: pensamentos, rascunhos, listas e fragmentos.
- `Diário/`: registro cronológico, sessões, tarefas e acontecimentos.
- `2 - Material fonte/`: PDFs, páginas, livros e anotações de leitura.

### 3.2 Conhecimento

- `3 - Notas completas/`: notas atômicas ou sínteses maduras.
- `Projects/`: contexto operacional, decisões e resultados por projeto.
- `Indexes/`: mapas de conteúdo e dashboards.

### 3.3 Controle da automação

Criar dentro da vault:

```text
Sistema/
├── Caixa de lapidação.md
├── Revisão semanal.md
├── Radar de pensamentos.md
├── Log de automações.md
└── Sugestões de links.md
```

Esses arquivos são filas e relatórios. Não são a fonte primária do conhecimento.

## 4. Metadados mínimos

### 4.1 Nota bruta

```yaml
---
type: fleeting
status: inbox
created: YYYY-MM-DD
updated: YYYY-MM-DD
topics: []
projects: []
source_notes: []
---
```

Valores de `status`:

- `inbox`: ainda não triada;
- `incubating`: vale manter, mas ainda está imatura;
- `ready`: candidata a lapidação;
- `processed`: originou ou foi incorporada a uma nota completa;
- `archived`: não requer trabalho adicional.

### 4.2 Nota completa

```yaml
---
type: evergreen
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
topics: []
projects: []
source_notes:
  - "[[Nome da nota bruta]]"
confidence: medium
---
```

A nota completa deve conter:

```markdown
# Título declarativo

## Ideia central

## Desenvolvimento

## Evidências e fontes

## Relações

## Questões em aberto
```

`confidence` descreve a maturidade da síntese, não a veracidade absoluta: `low`, `medium`, `high`.

### 4.3 Tarefas

Usar o formato do plugin Tasks e manter a tarefa na nota que fornece o contexto:

```markdown
- [ ] Formular hipótese sobre X #projeto/exemplo 📅 YYYY-MM-DD
- [x] Comparar abordagens A e B ✅ YYYY-MM-DD
```

Convenções sugeridas:

- projeto: `#projeto/<nome>`;
- área: `#area/<nome>`;
- estado especial: `#waiting`, `#someday`;
- prioridade e datas: sintaxe nativa do Tasks.

Não usar `#tasks` como requisito global. O checkbox já identifica uma tarefa e tags devem carregar contexto.

## 5. Dashboards

### 5.1 `Indexes/Tarefas.md`

```markdown
# Tarefas

## Atrasadas

```tasks
not done
due before today
sort by due
```

## Hoje

```tasks
not done
(due today) OR (scheduled today)
sort by priority
```

## Próximas

```tasks
not done
due after today
due before in 14 days
sort by due
```

## Sem data

```tasks
not done
no due date
path does not include Templates
sort by path
```

## Concluídas recentemente

```tasks
done
done after 7 days ago
sort by done reverse
```
```

### 5.2 `Sistema/Caixa de lapidação.md`

```markdown
# Caixa de lapidação

```dataview
TABLE status, file.mtime AS "Atualizada", topics AS "Temas", projects AS "Projetos"
FROM "1 - Notas brutas"
WHERE type = "fleeting" AND status != "processed" AND status != "archived"
SORT choice(status = "ready", 0, choice(status = "inbox", 1, 2)) ASC, file.mtime DESC
```
```

### 5.3 `Sistema/Radar de pensamentos.md`

O arquivo é atualizado pela automação semanal e apresenta:

- temas mais recorrentes nos últimos 7, 30 e 90 dias;
- ideias que reapareceram em notas distintas;
- perguntas ainda sem resposta;
- temas que cresceram ou perderam atividade;
- notas isoladas com potencial de conexão;
- projetos associados a cada tendência.

O radar deve sempre listar os wikilinks que sustentam cada conclusão.

## 6. Workflows

### 6.1 Captura diária

1. Criar livremente em `1 - Notas brutas/`.
2. O template adiciona apenas metadados mínimos.
3. Não exigir título perfeito, tags ou links durante a captura.

### 6.2 Triagem de inbox

Comando proposto: `obsidian-brain:triage`.

1. Ler notas com `status: inbox`.
2. Para cada nota, sugerir título, tópicos, projeto e destino.
3. Identificar tarefas explícitas, sem transformar desejos vagos em compromissos.
4. Classificar como `incubating`, `ready`, `processed` ou `archived`.
5. Aplicar mudanças simples de metadados automaticamente.
6. Exigir revisão antes de mover conteúdo ou gerar uma nota completa.

Saída compacta:

```text
Nota: [[nome atual]]
Sugestão: "novo título"
Destino: ready
Tarefas encontradas: 2
Conexões candidatas: [[A]], [[B]]
Motivo: ...
```

### 6.3 Lapidação

Comando proposto: `obsidian-brain:refine <nota>`.

1. Ler a nota bruta integralmente.
2. Buscar notas completas, materiais fonte e projetos relacionados.
3. Separar afirmações, hipóteses, dúvidas, tarefas e referências.
4. Escolher uma ação:
   - criar nova nota completa;
   - incorporar a uma nota completa existente;
   - dividir em duas ou mais notas atômicas;
   - manter incubando por falta de substância.
5. Gerar um rascunho com `source_notes` e links bidirecionais.
6. Mostrar diff ou resumo da transformação.
7. Somente após aprovação, gravar em `3 - Notas completas/`.
8. Marcar a origem como `processed` e adicionar `developed_into`.

Nunca substituir a nota bruta pela versão lapidada.

### 6.4 Linkagem

Comando proposto: `obsidian-brain:connect <nota ou pasta>`.

Cada link sugerido recebe um tipo e uma justificativa:

- `supports`: fornece evidência;
- `contradicts`: apresenta tensão ou conflito;
- `extends`: desenvolve a ideia;
- `example_of`: é um caso da ideia;
- `related`: relação temática forte, quando nenhum tipo mais preciso se aplica.

Formato em `## Relações`:

```markdown
- extends [[Outra nota]] — amplia a hipótese ao considerar X.
- contradicts [[Terceira nota]] — assume Y, enquanto esta nota depende de não-Y.
```

Não adicionar links apenas porque duas notas compartilham uma palavra-chave.

### 6.5 Tracking de pensamentos

Comando proposto: `obsidian-brain:reflect`.

Janela padrão: 30 dias. Comparar também com os 30 dias anteriores.

Extrair:

- tópicos frequentes;
- tópicos novos;
- tópicos abandonados;
- perguntas recorrentes;
- hipóteses que mudaram;
- decisões tomadas;
- tarefas geradas e concluídas;
- notas brutas que convergiram para notas completas.

Gerar um snapshot em `Diário/Reflexões/YYYY-MM.md` e atualizar `Sistema/Radar de pensamentos.md`. Toda tendência precisa citar as notas que a sustentam. A ausência de menção não deve ser interpretada automaticamente como perda de interesse.

### 6.6 Revisão semanal

Comando proposto: `obsidian-brain:weekly-review`.

Checklist:

1. tarefas atrasadas, próximas e sem data;
2. tarefas concluídas na semana;
3. notas `inbox` e `ready`;
4. notas sem links;
5. perguntas recorrentes;
6. projetos ativos sem atualização recente;
7. três prioridades sugeridas para a próxima semana.

A automação prepara a revisão, mas o usuário decide prioridades e arquivamentos.

## 7. Evolução da skill existente

A skill atual está bem estruturada para registrar sessões de agentes, contexto, decisões e logs de projeto. Ela ainda não cobre o ciclo principal desta vault: nota bruta → triagem → lapidação → conexão → reflexão.

Adicionar as seguintes skills especializadas:

```text
obsidian-brain-triage/
obsidian-brain-refine/
obsidian-brain-connect/
obsidian-brain-reflect/
obsidian-brain-weekly-review/
```

Adicionar referências compartilhadas:

```text
references/note-lifecycle.md
references/task-policy.md
references/link-policy.md
references/reflection.md
references/safety-and-provenance.md
```

Atualizar o dispatcher para reconhecer:

| Intenção | Skill |
|---|---|
| organizar inbox, triar notas | `triage` |
| lapidar, completar uma nota | `refine` |
| ligar ideias, achar conexões | `connect` |
| o que tenho pensado, tendências | `reflect` |
| revisão semanal | `weekly-review` |

## 8. Segurança editorial

### Pode ser automático

- criar dashboards;
- completar metadados ausentes;
- gerar relatórios em `Sistema/`;
- sugerir títulos, tags e links;
- registrar tarefas explicitamente escritas;
- criar rascunhos novos sem substituir arquivos.

### Requer aprovação

- mover ou renomear notas;
- marcar nota como `processed` ou `archived`;
- incorporar conteúdo a uma nota completa existente;
- criar links no corpo de notas;
- converter linguagem vaga em tarefa;
- dividir ou mesclar notas.

### Nunca automático

- apagar nota bruta;
- remover trechos da fonte;
- inventar citações ou referências;
- tratar inferência como fato;
- marcar tarefa como concluída sem evidência;
- reescrever em massa toda a vault de uma vez.

## 9. Implantação em fases

### Fase 1 — fundação

- criar templates de nota bruta e completa;
- criar `Indexes/Tarefas.md`;
- criar `Sistema/Caixa de lapidação.md`;
- padronizar apenas notas novas;
- implementar `triage` em modo sugestão.

### Fase 2 — lapidação assistida

- implementar `refine` com rascunho e aprovação;
- implementar `connect` com justificativas;
- testar em 5 a 10 notas, sem migração em massa.

### Fase 3 — reflexão

- implementar `reflect` e `weekly-review`;
- criar snapshots mensais;
- ajustar propriedades e relatórios com base no uso real.

### Fase 4 — automação recorrente opcional

- triagem diária apenas para notas novas;
- revisão semanal agendada;
- relatório mensal de tendências;
- nenhuma alteração destrutiva em execução agendada.

## 10. Base de conhecimento, mensageria e grafo local

### Consulta por Telegram e Discord

O Hermes Gateway executa o mesmo agente, skills e ferramentas nos dois canais. A integração usa três comandos explícitos:

- `obsidian-brain:query`: busca híbrida e resposta com fontes da vault;
- `obsidian-brain:capture`: salva apenas conteúdo explicitamente enviado para captura;
- `obsidian-brain:graph`: mostra wikilinks e vizinhos semânticos.

DMs autorizadas podem consultar a vault, excluindo credenciais. Canais compartilhados não expõem `Diário/` ou notas privadas e não são arquivados passivamente.

### Índice híbrido gratuito

```text
Markdown da vault
    ├── SQLite FTS5            → correspondência lexical
    ├── FastEmbed/ONNX         → embeddings neurais multilíngues, 384 dimensões
    └── tabela de wikilinks    → grafo explícito
                 ↓
          ranking híbrido
                 ↓
       leitura das notas-fonte
                 ↓
       resposta citada pelo Hermes
```

Modelo padrão: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`. O download é feito uma vez e a inferência roda localmente, sem custo de API. As assinaturas Codex/ChatGPT e Claude podem ser usadas pelo Hermes para síntese, extração de conceitos e respostas, mas seus logins OAuth de assinatura não devem ser tratados como APIs de embeddings. Nous Portal pode expor `/v1/embeddings` dependendo do plano, mas não é necessário para esta implementação.

O índice exclui pastas geradas, ambientes virtuais, lixeira e notas com nomes ou padrões de conteúdo semelhantes a credenciais.

## 11. Critérios de sucesso

Após duas semanas de uso:

- toda tarefa aberta aparece em um dashboard;
- tarefas concluídas podem ser revisadas por período;
- notas brutas continuam rápidas de criar;
- cada nota completa aponta para suas fontes;
- sugestões de links trazem justificativa;
- o radar cita evidências e não inventa tendências;
- nenhuma automação apaga ou sobrescreve material bruto;
- a taxonomia continua pequena o suficiente para ser usada de verdade.
