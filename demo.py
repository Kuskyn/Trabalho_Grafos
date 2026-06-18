"""Programa de demonstração em terminal da biblioteca ``graphs``.

Script linear e determinístico (sem entrada interativa) que percorre as
principais funcionalidades da biblioteca, construindo o mesmo grafo de
exemplo nas duas representações disponíveis (matriz de adjacência e lista
de adjacência) e comparando os resultados lado a lado.

Execução:
    py demo.py
"""

import os
import sys

from graphs import (
    AdjacencyListGraph,
    AdjacencyMatrixGraph,
    SelfLoopError,
)

# Garante saída em UTF-8 no terminal, independentemente da codificação
# padrão do console do sistema operacional (ex.: cp1252/cp850 no Windows).
sys.stdout.reconfigure(encoding="utf-8")

# Arestas do grafo de exemplo: um ciclo (0->1->2->3->4->0) mais uma corda
# (1->3). O ciclo, por si só, já torna o grafo fortemente conectado (há
# caminho de ida e volta entre quaisquer dois vértices seguindo o sentido
# das arestas); a corda 1->3 é apenas um atalho adicional dentro do ciclo.
SAMPLE_EDGES = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (1, 3)]
SAMPLE_VERTEX_COUNT = 5


def section(title: str) -> None:
    """Imprime um cabeçalho de seção padronizado."""
    print("\n=== " + title + " ===")


def buildSampleGraphs():
    """Cria o grafo de exemplo nas duas representações, com as mesmas arestas."""
    matrixGraph = AdjacencyMatrixGraph(SAMPLE_VERTEX_COUNT)
    listGraph = AdjacencyListGraph(SAMPLE_VERTEX_COUNT)
    for u, v in SAMPLE_EDGES:
        matrixGraph.addEdge(u, v)
        listGraph.addEdge(u, v)
    return matrixGraph, listGraph


def demoCreationMatrix() -> None:
    section("1. Criação via matriz")
    matrixGraph = AdjacencyMatrixGraph(SAMPLE_VERTEX_COUNT)
    print(f"AdjacencyMatrixGraph criado com {SAMPLE_VERTEX_COUNT} vértices.")
    print(f"matrix: getVertexCount() = {matrixGraph.getVertexCount()}")


def demoCreationList() -> None:
    section("2. Criação via lista")
    listGraph = AdjacencyListGraph(SAMPLE_VERTEX_COUNT)
    print(f"AdjacencyListGraph criado com {SAMPLE_VERTEX_COUNT} vértices.")
    print(f"list:   getVertexCount() = {listGraph.getVertexCount()}")

    print(
        "\nAdicionando as mesmas arestas em ambas as representações: "
        f"{SAMPLE_EDGES}"
    )
    matrixGraph, listGraph = buildSampleGraphs()
    print(f"matrix: getEdgeCount() = {matrixGraph.getEdgeCount()}")
    print(f"list:   getEdgeCount() = {listGraph.getEdgeCount()}")


def demoEdgeInsertionRemoval() -> None:
    section("3. Inserção/remoção de arestas")
    matrixGraph, listGraph = buildSampleGraphs()

    u, v = 2, 4
    print(f"Antes de addEdge({u}, {v}):")
    print(f"matrix: hasEdge({u}, {v}) = {matrixGraph.hasEdge(u, v)}")
    print(f"list:   hasEdge({u}, {v}) = {listGraph.hasEdge(u, v)}")

    matrixGraph.addEdge(u, v)
    listGraph.addEdge(u, v)
    print(f"\nDepois de addEdge({u}, {v}):")
    print(f"matrix: hasEdge({u}, {v}) = {matrixGraph.hasEdge(u, v)}")
    print(f"list:   hasEdge({u}, {v}) = {listGraph.hasEdge(u, v)}")

    countBefore_matrix = matrixGraph.getEdgeCount()
    countBefore_list = listGraph.getEdgeCount()
    matrixGraph.addEdge(u, v)
    listGraph.addEdge(u, v)
    print(f"\nChamando addEdge({u}, {v}) novamente (idempotência):")
    print(
        f"matrix: getEdgeCount() = {matrixGraph.getEdgeCount()} "
        f"(antes: {countBefore_matrix}, inalterado)"
    )
    print(
        f"list:   getEdgeCount() = {listGraph.getEdgeCount()} "
        f"(antes: {countBefore_list}, inalterado)"
    )

    matrixGraph.removeEdge(u, v)
    listGraph.removeEdge(u, v)
    print(f"\nDepois de removeEdge({u}, {v}):")
    print(
        f"matrix: hasEdge({u}, {v}) = {matrixGraph.hasEdge(u, v)}, "
        f"getEdgeCount() = {matrixGraph.getEdgeCount()}"
    )
    print(
        f"list:   hasEdge({u}, {v}) = {listGraph.hasEdge(u, v)}, "
        f"getEdgeCount() = {listGraph.getEdgeCount()}"
    )

    absentU, absentV = 0, 3
    countBefore_matrix = matrixGraph.getEdgeCount()
    countBefore_list = listGraph.getEdgeCount()
    matrixGraph.removeEdge(absentU, absentV)
    listGraph.removeEdge(absentU, absentV)
    print(
        f"\nremoveEdge({absentU}, {absentV}) em aresta ausente é um no-op "
        "inofensivo:"
    )
    print(
        f"matrix: getEdgeCount() = {matrixGraph.getEdgeCount()} "
        f"(antes: {countBefore_matrix}, inalterado)"
    )
    print(
        f"list:   getEdgeCount() = {listGraph.getEdgeCount()} "
        f"(antes: {countBefore_list}, inalterado)"
    )


def demoSuccessorsPredecessors() -> None:
    section("4. Sucessores/predecessores")
    matrixGraph, listGraph = buildSampleGraphs()

    pairs = [(1, 2), (1, 3), (2, 1)]
    for u, v in pairs:
        print(f"Par (u={u}, v={v}):")
        print(
            f"matrix: isSuccessor({u}, {v}) = {matrixGraph.isSuccessor(u, v)}, "
            f"isPredecessor({u}, {v}) = {matrixGraph.isPredecessor(u, v)}"
        )
        print(
            f"list:   isSuccessor({u}, {v}) = {listGraph.isSuccessor(u, v)}, "
            f"isPredecessor({u}, {v}) = {listGraph.isPredecessor(u, v)}"
        )


def demoInOutDegree() -> None:
    section("5. In/out-degree")
    matrixGraph, listGraph = buildSampleGraphs()

    for vertex in range(SAMPLE_VERTEX_COUNT):
        print(
            f"Vértice {vertex} -- "
            f"matrix: in={matrixGraph.getVertexInDegree(vertex)}, "
            f"out={matrixGraph.getVertexOutDegree(vertex)} | "
            f"list: in={listGraph.getVertexInDegree(vertex)}, "
            f"out={listGraph.getVertexOutDegree(vertex)}"
        )


def demoVertexWeights() -> None:
    section("6. Pesos de vértices")
    matrixGraph, listGraph = buildSampleGraphs()

    vertex = 2
    print(f"Peso padrão do vértice {vertex}:")
    print(f"matrix: getVertexWeight({vertex}) = {matrixGraph.getVertexWeight(vertex)}")
    print(f"list:   getVertexWeight({vertex}) = {listGraph.getVertexWeight(vertex)}")

    newWeight = 3.5
    matrixGraph.setVertexWeight(vertex, newWeight)
    listGraph.setVertexWeight(vertex, newWeight)
    print(f"\nApós setVertexWeight({vertex}, {newWeight}):")
    print(f"matrix: getVertexWeight({vertex}) = {matrixGraph.getVertexWeight(vertex)}")
    print(f"list:   getVertexWeight({vertex}) = {listGraph.getVertexWeight(vertex)}")


def demoEdgeWeights() -> None:
    section("7. Pesos de arestas")
    matrixGraph, listGraph = buildSampleGraphs()

    u, v = 0, 2
    matrixGraph.addEdge(u, v)
    listGraph.addEdge(u, v)
    print(f"Peso padrão da aresta nova ({u}, {v}):")
    print(f"matrix: getEdgeWeight({u}, {v}) = {matrixGraph.getEdgeWeight(u, v)}")
    print(f"list:   getEdgeWeight({u}, {v}) = {listGraph.getEdgeWeight(u, v)}")

    newWeight = 7.25
    matrixGraph.setEdgeWeight(u, v, newWeight)
    listGraph.setEdgeWeight(u, v, newWeight)
    print(f"\nApós setEdgeWeight({u}, {v}, {newWeight}):")
    print(f"matrix: getEdgeWeight({u}, {v}) = {matrixGraph.getEdgeWeight(u, v)}")
    print(f"list:   getEdgeWeight({u}, {v}) = {listGraph.getEdgeWeight(u, v)}")


def demoEmptyGraph() -> None:
    section("8. Grafo vazio")
    emptyMatrixGraph = AdjacencyMatrixGraph(SAMPLE_VERTEX_COUNT)
    emptyListGraph = AdjacencyListGraph(SAMPLE_VERTEX_COUNT)
    matrixGraph, listGraph = buildSampleGraphs()

    print("Grafo recém-criado, sem arestas:")
    print(f"matrix: isEmptyGraph() = {emptyMatrixGraph.isEmptyGraph()}")
    print(f"list:   isEmptyGraph() = {emptyListGraph.isEmptyGraph()}")

    print("\nGrafo de exemplo, com arestas:")
    print(f"matrix: isEmptyGraph() = {matrixGraph.isEmptyGraph()}")
    print(f"list:   isEmptyGraph() = {listGraph.isEmptyGraph()}")


def demoCompleteGraph() -> None:
    section("9. Grafo completo")
    n = 3
    completeMatrixGraph = AdjacencyMatrixGraph(n)
    completeListGraph = AdjacencyListGraph(n)
    for u in range(n):
        for v in range(n):
            if u != v:
                completeMatrixGraph.addEdge(u, v)
                completeListGraph.addEdge(u, v)

    print(f"K{n} direcionado (todas as {n * (n - 1)} arestas possíveis):")
    print(f"matrix: isCompleteGraph() = {completeMatrixGraph.isCompleteGraph()}")
    print(f"list:   isCompleteGraph() = {completeListGraph.isCompleteGraph()}")

    matrixGraph, listGraph = buildSampleGraphs()
    print("\nGrafo de exemplo (não possui todas as arestas possíveis):")
    print(f"matrix: isCompleteGraph() = {matrixGraph.isCompleteGraph()}")
    print(f"list:   isCompleteGraph() = {listGraph.isCompleteGraph()}")


def demoConnectivity() -> None:
    section("10. Grafo conectado")
    print(
        "Conectividade fraca (weak): trata as arestas como não direcionadas "
        "e verifica se há um caminho entre quaisquer dois vértices.\n"
        "Conectividade forte (strong): exige que todo vértice seja "
        "alcançável a partir do vértice 0 e que o vértice 0 seja alcançável "
        "a partir de todo vértice, respeitando o sentido das arestas."
    )

    matrixGraph, listGraph = buildSampleGraphs()
    print("\nGrafo de exemplo (ciclo 0->1->2->3->4->0 + corda 1->3):")
    print(
        f"matrix: isConnected(strong=False) = {matrixGraph.isConnected(strong=False)}, "
        f"isConnected(strong=True) = {matrixGraph.isConnected(strong=True)}"
    )
    print(
        f"list:   isConnected(strong=False) = {listGraph.isConnected(strong=False)}, "
        f"isConnected(strong=True) = {listGraph.isConnected(strong=True)}"
    )

    cycleMatrixGraph = AdjacencyMatrixGraph(4)
    cycleListGraph = AdjacencyListGraph(4)
    cycleEdges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    for u, v in cycleEdges:
        cycleMatrixGraph.addEdge(u, v)
        cycleListGraph.addEdge(u, v)
    print("\nCiclo direcionado 0->1->2->3->0 (fortemente conectado):")
    print(
        f"matrix: isConnected(strong=False) = {cycleMatrixGraph.isConnected(strong=False)}, "
        f"isConnected(strong=True) = {cycleMatrixGraph.isConnected(strong=True)}"
    )
    print(
        f"list:   isConnected(strong=False) = {cycleListGraph.isConnected(strong=False)}, "
        f"isConnected(strong=True) = {cycleListGraph.isConnected(strong=True)}"
    )

    disconnectedMatrixGraph = AdjacencyMatrixGraph(4)
    disconnectedListGraph = AdjacencyListGraph(4)
    disconnectedEdges = [(0, 1), (2, 3)]
    for u, v in disconnectedEdges:
        disconnectedMatrixGraph.addEdge(u, v)
        disconnectedListGraph.addEdge(u, v)
    print("\nGrafo desconectado (duas componentes: 0->1 e 2->3):")
    print(
        f"matrix: isConnected(strong=False) = {disconnectedMatrixGraph.isConnected(strong=False)}, "
        f"isConnected(strong=True) = {disconnectedMatrixGraph.isConnected(strong=True)}"
    )
    print(
        f"list:   isConnected(strong=False) = {disconnectedListGraph.isConnected(strong=False)}, "
        f"isConnected(strong=True) = {disconnectedListGraph.isConnected(strong=True)}"
    )


def demoExportToGephi() -> None:
    section("11. Exportação para Gephi")
    matrixGraph, _listGraph = buildSampleGraphs()

    outputPath = "demo_graph.gexf"
    matrixGraph.exportToGEPHI(outputPath)
    absolutePath = os.path.abspath(outputPath)
    print(f"Grafo de exemplo (representação por matriz) exportado para: {absolutePath}")
    print(
        "O arquivo está no formato GEXF 1.2 e pode ser aberto/importado "
        "diretamente no Gephi (File > Open)."
    )
    print(
        "Observação: exportar a versão por lista de adjacência do mesmo "
        "grafo produziria um arquivo GEXF idêntico, pois ambas as "
        "representações compartilham a mesma API pública."
    )


def demoSelfLoopGuardedExample() -> None:
    section("Extra: exceção de self-loop (exemplo opcional)")
    matrixGraph, _listGraph = buildSampleGraphs()
    try:
        matrixGraph.addEdge(2, 2)
    except SelfLoopError as error:
        print(f"SelfLoopError capturada como esperado: {error}")


def main() -> None:
    demoCreationMatrix()
    demoCreationList()
    demoEdgeInsertionRemoval()
    demoSuccessorsPredecessors()
    demoInOutDegree()
    demoVertexWeights()
    demoEdgeWeights()
    demoEmptyGraph()
    demoCompleteGraph()
    demoConnectivity()
    demoExportToGephi()
    demoSelfLoopGuardedExample()


if __name__ == "__main__":
    main()
