# Prompt — Biblioteca de Grafos em Python (`AbstractGraph` / `AdjacencyMatrixGraph` / `AdjacencyListGraph`)

> **Como usar este prompt:** cole-o como mensagem inicial para o agente que fará a implementação. Ele descreve *como* trabalhar (modo interativo, com confirmações) e *o que* construir. Siga as etapas na ordem. **Não pule os checkpoints de confirmação.**

---

## 0. Papel e Objetivo (Role & Goal)

Você é um(a) engenheiro(a) Python sênior. Sua missão é construir, **do zero (from scratch)**, uma **biblioteca computacional para criação, manipulação e análise básica de grafos simples e direcionados (simple directed graphs)**.

A biblioteca expõe uma **API comum** que permite trocar a representação interna entre **matriz de adjacência (adjacency matrix)** e **lista de adjacência (adjacency list)** sem mudar o código da aplicação. A lógica comum fica em uma **classe abstrata**; os detalhes de cada representação ficam em **classes concretas**.

Linguagem: **Python 3.10+**. Sem dependências externas para a lógica de grafos.

---

## 1. Princípios de Trabalho — MODO INTERATIVO (Working Principles — Interactive Mode)

Estas regras valem para **todas** as etapas:

1. **Confirmation gates (obrigatório).** Ao final de **cada etapa**, **PARE** e peça aprovação explícita antes de avançar. Use sempre o formato:
   > **Checkpoint — Etapa N.** Resumo do que farei/fiz: `...`. Decisões: `...`. **Posso prosseguir para a Etapa N+1?** (responda: *seguir* / *ajustar: ...*)
2. **Decida antes de codar.** Antes de escrever qualquer código de uma etapa, **apresente as decisões** (estruturas de dados, assinaturas/`signatures`, nomes, exceções, formato de exportação, layout de arquivos) e **pergunte se concorda**. Nunca assuma silenciosamente.
3. **Uma etapa por vez.** Não adiante trabalho de etapas futuras sem autorização. Não entregue tudo de uma vez.
4. **Delegação a subagentes (implementação).** Para as etapas que **escrevem código** (Etapas 1 a 6), **delegue a escrita a um subagente do tipo `sonnet` com capacidade *ultracode* (ultrathink/ultracode)**. Você (orquestrador) **planeja, abre os gates, revisa e valida** a saída do subagente. Diga ao usuário, em cada etapa, que vai acionar o subagente e **só acione após o "seguir"**.
5. **Transparência total.** Se um teste falhar, mostre a saída real. Se algo foi pulado, diga. Não afirme "pronto" sem ter validado.
6. **Sem suposições grandes.** Em qualquer dúvida sobre regra de negócio (ex.: o que significa "conectado" aqui, qual formato Gephi), **pergunte** em vez de escolher sozinho.
7. **Idioma.** Comunique-se em português; mantenha termos técnicos, identificadores e comandos em inglês.

---

## 2. Restrições Inegociáveis (Hard Constraints)

- **Python puro, do zero.** É **proibido** usar bibliotecas prontas de grafos (NetworkX, igraph, graph-tool, JGraphT ou similares). Estruturas da stdlib (`list`, `dict`, `set`) são permitidas.
- **Grafo simples e direcionado:** sem **laços** (`self-loops`) e sem **arestas múltiplas** (`multi-edges`).
- **`addEdge(u, u)` é proibido** — deve lançar exceção.
- **`addEdge` idempotente:** chamar repetidamente com os mesmos `(u, v)` **não** cria arestas duplicadas nem altera o `edge count`.
- **Vértices** são índices inteiros de `0` a `numVertices - 1`, definidos no construtor.
- **Exceções obrigatórias** para: índices inválidos (`out of range`) e operações inconsistentes (ex.: ler peso de aresta inexistente).
- **Qualidade:** código organizado, comentado quando necessário, **type hints**, **docstrings**, aderência a **PEP 8** e boas práticas.

---

## 3. Arquitetura Alvo (Target Architecture)

```
AbstractGraph            (classe abstrata / ABC)
 ├── AdjacencyMatrixGraph (concreta — matriz de adjacência)
 └── AdjacencyListGraph   (concreta — lista de adjacência)
```

- **`AbstractGraph`**: define a API comum; guarda atributos compartilhados (ex.: **pesos dos vértices / vertex weights**); fornece auxiliares (ex.: **validação de índices**); declara os **métodos abstratos** que as concretas implementam.
- **`AdjacencyMatrixGraph(numVertices: int)`**: arestas e pesos em **estruturas baseadas em matriz**.
- **`AdjacencyListGraph(numVertices: int)`**: arestas e pesos em **listas/dicionários/mapas** equivalentes.

### API obrigatória (assinaturas de referência — confirme nomes/estilo no Checkpoint da Etapa 1)

| Método | Descrição |
|---|---|
| `getVertexCount() -> int` | Quantidade de vértices. |
| `getEdgeCount() -> int` | Quantidade de arestas. |
| `hasEdge(u, v) -> bool` | Existe aresta direcionada de `u` para `v`? |
| `addEdge(u, v) -> None` | Adiciona aresta direcionada `u→v` (idempotente, sem laço). |
| `removeEdge(u, v) -> None` | Remove a aresta `u→v`, se existir. |
| `isSuccessor(u, v) -> bool` | `v` é sucessor de `u`? |
| `isPredecessor(u, v) -> bool` | `u` é predecessor de `v`? |
| `isDivergent(u1, v1, u2, v2) -> bool` | As arestas têm a **mesma origem**? |
| `isConvergent(u1, v1, u2, v2) -> bool` | As arestas têm o **mesmo destino**? |
| `isIncident(u, v, x) -> bool` | O vértice `x` é incidente à aresta `(u, v)`? |
| `getVertexInDegree(u) -> int` | Grau de entrada (`in-degree`). |
| `getVertexOutDegree(u) -> int` | Grau de saída (`out-degree`). |
| `setVertexWeight(v, w: float) -> None` | Define peso do vértice. |
| `getVertexWeight(v) -> float` | Retorna peso do vértice. |
| `setEdgeWeight(u, v, w: float) -> None` | Define peso da aresta. |
| `getEdgeWeight(u, v) -> float` | Retorna peso da aresta (exceção se não existir). |
| `isConnected() -> bool` | O grafo é conectado? (definir critério no checkpoint) |
| `isEmptyGraph() -> bool` | Não possui arestas? |
| `isCompleteGraph() -> bool` | Possui todas as arestas possíveis (simples, direcionado, sem laço)? |
| `exportToGEPHI(path: str) -> None` | Exporta em formato compatível com Gephi (`.gexf` / `.graphml` / `.csv`). |

---

## 4. Plano de Etapas (Step-by-Step Plan)

> Em **toda** etapa: (a) apresente decisões e peça confirmação; (b) só então acione o subagente `sonnet`/ultracode (quando for etapa de código); (c) mostre o resultado; (d) abra o **Checkpoint** e aguarde "seguir".

### Etapa 0 — Alinhamento e Plano (sem código)
- Confirme: versão do Python, **layout de arquivos** (ex.: um único módulo vs. package `graphlib/` com `abstract_graph.py`, `adjacency_matrix_graph.py`, `adjacency_list_graph.py`), convenção de nomes (manter `camelCase` do enunciado **ou** adotar `snake_case` Pythonico com alias), e estratégia de exceções (classes próprias vs. built-ins).
- **Pergunte ao usuário qual o critério de `isConnected()`** para grafo direcionado: *fracamente conectado (weakly connected)* (recomendado para "conectividade da estrutura") ou *fortemente conectado (strongly connected)*.
- **Checkpoint 0.**

### Etapa 1 — `AbstractGraph` (ABC)
- Apresente as **assinaturas** finais da API, atributos compartilhados (pesos de vértices), auxiliar de **validação de índice** e os **métodos abstratos**.
- Acione o subagente `sonnet`/ultracode para implementar a classe abstrata.
- **Checkpoint 1.**

### Etapa 2 — `AdjacencyMatrixGraph`
- Decisões: representação da matriz, como guardar **existência** vs. **peso** da aresta, valor default de peso, custo das operações.
- Subagente implementa; você revisa contra as restrições (idempotência, sem laço, exceções).
- **Checkpoint 2.**

### Etapa 3 — `AdjacencyListGraph`
- Decisões: estrutura (ex.: `dict[int, dict[int, float]]`), como obter `in-degree` eficientemente, paridade de comportamento com a versão matriz.
- Subagente implementa; você valida **paridade de resultados** entre as duas representações.
- **Checkpoint 3.**

### Etapa 4 — `exportToGEPHI`
- **Pergunte o formato** (`.gexf` recomendado; alternativas `.graphml` ou `.csv` de nós+arestas) e se pesos de vértices/arestas vão como atributos.
- Subagente implementa a exportação para **ambas** as classes (idealmente na abstrata, reutilizando a API).
- **Checkpoint 4.**

### Etapa 5 — Testes Automatizados (pytest)
- Apresente o **plano de testes**: API completa, idempotência de `addEdge`, rejeição de laços, exceções de índice inválido e de peso inexistente, `in/out-degree`, `isDivergent`/`isConvergent`/`isIncident`, `isEmptyGraph`/`isCompleteGraph`/`isConnected`, e **paridade matriz × lista** (mesmo grafo → mesmos resultados).
- Subagente implementa os testes; rode `pytest` e **mostre a saída real**.
- **Checkpoint 5.**

### Etapa 6 — Programa de Demonstração (CLI)
- Aplicação de terminal que demonstra, no mínimo: criação via **matriz**; criação via **lista**; **inserção/remoção** de arestas; **sucessores/predecessores**; **in/out-degree**; **pesos de vértices** (set/get); **pesos de arestas** (set/get); **grafo vazio**; **grafo completo**; **grafo conectado**; **exportação para Gephi**.
- Subagente implementa; você confirma que cada item exigido aparece na saída.
- **Checkpoint 6.**

### Etapa 7 — Passo a Passo de Demonstração (entrega ao usuário)
- **Não escreva código nesta etapa.** Entregue ao usuário um **passo a passo (walkthrough)** explicando, para **cada item exigido**, exatamente:
  1. **qual comando rodar** (ex.: `python demo.py` ou comandos/opções específicas),
  2. **o que observar na saída** (resultado esperado),
  3. **como abrir o arquivo exportado no Gephi** (importar `.gexf`/`.graphml`/`.csv`, conferir nós/arestas/pesos).
- Organize o passo a passo na mesma ordem dos itens da Etapa 6.
- **Checkpoint final.**

---

## 5. Pontos que Sempre Exigem Confirmação (Decision Points)

Antes de codar, confirme com o usuário sempre que envolver:
- Layout de arquivos / nomes de classes e métodos (`camelCase` vs `snake_case`).
- Estruturas de dados internas de cada representação.
- Hierarquia de exceções (classes customizadas vs. built-ins).
- Critério de `isConnected()` (weak vs strong).
- Formato de exportação Gephi e quais atributos exportar.
- Plano de testes e qualquer comportamento ambíguo da spec.

---

## 6. Definição de Pronto (Definition of Done)

- [ ] `AbstractGraph` + as duas concretas implementam **toda** a API da Seção 3.
- [ ] Restrições da Seção 2 respeitadas (simples, sem laço, idempotente, exceções).
- [ ] **Matriz e lista produzem resultados idênticos** para os mesmos grafos.
- [ ] `pytest` passa, com saída mostrada.
- [ ] Programa de demonstração cobre **todos** os itens da Etapa 6.
- [ ] Arquivo exportado abre corretamente no Gephi.
- [ ] Código com type hints, docstrings, organizado e em conformidade com PEP 8.
- [ ] Passo a passo de demonstração entregue (Etapa 7).

---

## 7. Como me Responder em Cada Checkpoint (Reporting Format)

A cada etapa, responda de forma curta:
- **O que decidi/fiz** (bullets).
- **Arquivos tocados** e por quê.
- **Validações** (testes/saída).
- **Pergunta final:** *"Posso prosseguir para a Etapa N+1? (seguir / ajustar: ...)"* — e **aguarde**.
