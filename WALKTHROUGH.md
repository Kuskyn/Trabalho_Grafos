# Passo a Passo de Demonstração — Biblioteca `graphs`

Este documento explica, item por item, **como executar a demonstração**, **o que observar na saída** e **como abrir o arquivo exportado no Gephi**. A ordem dos itens segue exatamente a do programa de demonstração (`demo.py`).

---

## Pré-requisitos

- **Python 3.10+** (aqui validado com Python 3.13). Neste ambiente o interpretador é chamado pelo launcher **`py`** (o comando `python` é um atalho da Microsoft Store e não funciona).
- Estar na pasta raiz do projeto:
  ```powershell
  cd "c:\Users\luina\Downloads\Grafos Workspace"
  ```
- **Opcional (para os testes):** `pytest` — já instalado (`py -m pip install pytest`).
- **Opcional (para o item 11):** [Gephi](https://gephi.org/) instalado, para abrir o arquivo `.gexf`.

---

## Comandos principais

| Objetivo | Comando |
|---|---|
| Rodar a demonstração completa | `py demo.py` |
| Rodar a suíte de testes | `py -m pytest -v` |

> A demonstração é **linear**: um único `py demo.py` imprime **todas** as seções de uma vez, de cima para baixo. Cada item abaixo corresponde a um cabeçalho `=== N. Título ===` na saída. Rode o comando uma vez e localize cada cabeçalho para conferir o resultado esperado.

---

## Itens da demonstração

### 1. Criação via matriz
- **Comando:** `py demo.py` → seção `=== 1. Criação via matriz ===`.
- **Observar:** um `AdjacencyMatrixGraph` é criado com 5 vértices.
- **Esperado:** `matrix: getVertexCount() = 5`.

### 2. Criação via lista
- **Comando:** seção `=== 2. Criação via lista ===`.
- **Observar:** um `AdjacencyListGraph` é criado com 5 vértices; em seguida as **mesmas arestas** `[(0,1),(1,2),(2,3),(3,4),(4,0),(1,3)]` são adicionadas às duas representações.
- **Esperado:** `list: getVertexCount() = 5`, e `getEdgeCount() = 6` para **ambas** (matrix e list) — confirmando paridade.

### 3. Inserção/remoção de arestas
- **Comando:** seção `=== 3. Inserção/remoção de arestas ===`.
- **Observar:** `hasEdge(2,4)` antes (False) e depois (True) de `addEdge`; **idempotência** (chamar `addEdge(2,4)` de novo não muda o `getEdgeCount`); `removeEdge(2,4)` volta `hasEdge` para False; e `removeEdge(0,3)` numa aresta **ausente** é um no-op inofensivo.
- **Esperado:** após o `addEdge` repetido, `getEdgeCount() = 7 (antes: 7, inalterado)`; após remover, `hasEdge(2,4) = False, getEdgeCount() = 6`; o no-op mantém `getEdgeCount() = 6`. Tudo igual em matrix e list.

### 4. Sucessores/predecessores
- **Comando:** seção `=== 4. Sucessores/predecessores ===`.
- **Observar:** `isSuccessor` / `isPredecessor` para os pares (1,2), (1,3) e (2,1).
- **Esperado:** (1,2) e (1,3) → `True/True`; (2,1) → `False/False` (não há aresta 2→1). Idêntico em matrix e list.

### 5. In/out-degree
- **Comando:** seção `=== 5. In/out-degree ===`.
- **Observar:** grau de entrada e de saída de cada vértice (0 a 4).
- **Esperado:**
  - Vértice 0 → in=1, out=1
  - Vértice 1 → in=1, out=2
  - Vértice 2 → in=1, out=1
  - Vértice 3 → in=2, out=1
  - Vértice 4 → in=1, out=1
  - Valores idênticos entre matrix e list.

### 6. Pesos de vértices
- **Comando:** seção `=== 6. Pesos de vértices ===`.
- **Observar:** peso padrão do vértice 2 e depois de `setVertexWeight(2, 3.5)`.
- **Esperado:** padrão `1.0`; após o set, `3.5`. Igual em matrix e list.

### 7. Pesos de arestas
- **Comando:** seção `=== 7. Pesos de arestas ===`.
- **Observar:** peso padrão da aresta nova (0,2) e depois de `setEdgeWeight(0, 2, 7.25)`.
- **Esperado:** padrão `1.0`; após o set, `7.25`. Igual em matrix e list.

### 8. Grafo vazio
- **Comando:** seção `=== 8. Grafo vazio ===`.
- **Observar:** `isEmptyGraph()` num grafo recém-criado e no grafo de exemplo.
- **Esperado:** recém-criado → `True`; grafo de exemplo (com arestas) → `False`. Igual em matrix e list.

### 9. Grafo completo
- **Comando:** seção `=== 9. Grafo completo ===`.
- **Observar:** `isCompleteGraph()` num K3 direcionado (todas as 6 arestas) e no grafo de exemplo.
- **Esperado:** K3 → `True`; grafo de exemplo → `False`. Igual em matrix e list.

### 10. Grafo conectado
- **Comando:** seção `=== 10. Grafo conectado ===`.
- **Observar:** explicação de conectividade fraca (weak) × forte (strong), seguida de três casos.
- **Esperado:**
  - Grafo de exemplo (ciclo + corda) → weak `True`, strong `True`.
  - Ciclo direcionado 0→1→2→3→0 → weak `True`, strong `True`.
  - Grafo desconectado (componentes 0→1 e 2→3) → weak `False`, strong `False`.
  - Idêntico entre matrix e list.

### 11. Exportação para Gephi
- **Comando:** seção `=== 11. Exportação para Gephi ===`.
- **Observar:** o grafo de exemplo é exportado para `demo_graph.gexf` na raiz do projeto; o caminho absoluto é impresso.
- **Esperado:** mensagem informando o caminho do arquivo (ex.: `...\Grafos Workspace\demo_graph.gexf`) e que ele está em formato GEXF 1.2. Veja a seção **"Abrindo no Gephi"** abaixo.

> *(Seção extra opcional na saída: demonstra que `addEdge(2, 2)` lança `SelfLoopError`, confirmando a proibição de laços.)*

---

## Abrindo o arquivo no Gephi

O arquivo gerado é `demo_graph.gexf` (formato **GEXF 1.2**, grafo **direcionado**), com **5 nós** e **6 arestas**.

1. **Abrir o Gephi** e ir em **File → Open…** (ou *Open Graph File…*).
2. Selecionar `demo_graph.gexf` na raiz do projeto.
3. Surge o **Import report**:
   - **Graph Type:** Directed (direcionado).
   - **Nodes:** 5, **Edges:** 6.
   - Escolher *New workspace* (ou *Append*) e clicar **OK**.
4. Na aba **Overview**, o grafo aparece. Aplique um layout (ex.: **ForceAtlas2**, no painel *Layout* → *Run*) para visualizar melhor o ciclo 0→1→2→3→4→0 com a corda 1→3.
5. Na aba **Data Laboratory**, conferir:
   - **Nodes:** colunas `Id`, `Label` e o atributo de peso de vértice **`weight`**.
   - **Edges:** colunas `Source`, `Target`, `Type` (Directed) e **`Weight`** (peso da aresta, atributo nativo do GEXF).

> **Observação importante sobre os pesos:** no `demo_graph.gexf` exportado pela demonstração, **todos os pesos (de vértices e de arestas) valem `1.0`**, pois o grafo de exemplo é exportado com os pesos padrão. Os pesos customizados (`setVertexWeight`/`setEdgeWeight`) são demonstrados nos itens 6 e 7 da saída do terminal e exercitados na suíte de testes (`tests/test_graph.py`), incluindo a verificação de que aparecem corretamente no GEXF.

---

## Verificação dos testes (opcional)

Para confirmar todo o contrato da biblioteca (idempotência, rejeição de laços, exceções, in/out-degree, conectividade weak/strong, exportação, e **paridade matriz × lista**):

```powershell
py -m pytest -v
```

**Esperado:** todos os testes passam (`161 passed`).
