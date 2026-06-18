"""Representação de grafo por lista de adjacência.

A classe :class:`AdjacencyListGraph` armazena as arestas em um dicionário de
adjacência por vértice (``self._adj``), mapeando cada destino ao peso da
aresta correspondente, e mantém um conjunto de predecessores por vértice
(``self._pred``) para consultas de grau de entrada em tempo O(1). Essa
representação favorece grafos esparsos, com espaço proporcional ao número de
arestas, em troca de um custo O(grau) para verificar a existência de uma
aresta específica.
"""

from collections.abc import Iterable

from .abstract_graph import AbstractGraph
from .exceptions import EdgeNotFoundError, SelfLoopError


class AdjacencyListGraph(AbstractGraph):
    """Grafo simples e direcionado representado por lista de adjacência.

    As arestas que saem de cada vértice são armazenadas em
    ``self._adj``, uma lista de dicionários ``destino -> peso``. Os
    predecessores de cada vértice são mantidos em ``self._pred``, uma lista
    de conjuntos, permitindo que ``getVertexInDegree`` seja O(1). A contagem
    de arestas é mantida incrementalmente em ``self._edgeCount`` para que
    ``getEdgeCount`` seja O(1).
    """

    def __init__(self, numVertices: int) -> None:
        """Inicializa o grafo com ``numVertices`` vértices e nenhuma aresta.

        Args:
            numVertices: Quantidade de vértices do grafo. Deve ser um
                inteiro maior ou igual a zero.

        Raises:
            ValueError: Se ``numVertices`` não for um ``int`` ou for
                negativo.
        """
        super().__init__(numVertices)
        n = self._numVertices
        self._adj: list[dict[int, float]] = [{} for _ in range(n)]
        self._pred: list[set[int]] = [set() for _ in range(n)]
        self._edgeCount: int = 0

    def getEdgeCount(self) -> int:
        """Retorna a quantidade de arestas do grafo."""
        return self._edgeCount

    def hasEdge(self, u: int, v: int) -> bool:
        """Verifica se existe aresta direcionada de ``u`` para ``v``.

        Raises:
            InvalidVertexError: Se ``u`` ou ``v`` for inválido.
        """
        self._validateVertex(u)
        self._validateVertex(v)
        return v in self._adj[u]

    def addEdge(self, u: int, v: int) -> None:
        """Adiciona a aresta direcionada ``u -> v``.

        A operação é idempotente: se a aresta já existir, seu peso atual é
        preservado e a contagem de arestas não é alterada.

        Raises:
            InvalidVertexError: Se ``u`` ou ``v`` for inválido.
            SelfLoopError: Se ``u == v``.
        """
        self._validateVertex(u)
        self._validateVertex(v)
        if u == v:
            raise SelfLoopError(f"Self-loops are not allowed (vertex {u})")
        if v in self._adj[u]:
            return
        self._adj[u][v] = self.DEFAULT_WEIGHT
        self._pred[v].add(u)
        self._edgeCount += 1

    def removeEdge(self, u: int, v: int) -> None:
        """Remove a aresta ``u -> v``, se existir.

        Raises:
            InvalidVertexError: Se ``u`` ou ``v`` for inválido.
        """
        self._validateVertex(u)
        self._validateVertex(v)
        if v not in self._adj[u]:
            return
        del self._adj[u][v]
        self._pred[v].discard(u)
        self._edgeCount -= 1

    def setEdgeWeight(self, u: int, v: int, w: float) -> None:
        """Define o peso da aresta ``u -> v``.

        Raises:
            InvalidVertexError: Se ``u`` ou ``v`` for inválido.
            EdgeNotFoundError: Se a aresta ``u -> v`` não existir.
        """
        self._validateVertex(u)
        self._validateVertex(v)
        if v not in self._adj[u]:
            raise EdgeNotFoundError(f"Edge ({u}, {v}) not found")
        self._adj[u][v] = w

    def getEdgeWeight(self, u: int, v: int) -> float:
        """Retorna o peso da aresta ``u -> v``.

        Raises:
            InvalidVertexError: Se ``u`` ou ``v`` for inválido.
            EdgeNotFoundError: Se a aresta ``u -> v`` não existir.
        """
        self._validateVertex(u)
        self._validateVertex(v)
        if v not in self._adj[u]:
            raise EdgeNotFoundError(f"Edge ({u}, {v}) not found")
        return self._adj[u][v]

    def getVertexInDegree(self, u: int) -> int:
        """Retorna o grau de entrada (in-degree) do vértice ``u``.

        Raises:
            InvalidVertexError: Se ``u`` for inválido.
        """
        self._validateVertex(u)
        return len(self._pred[u])

    def getVertexOutDegree(self, u: int) -> int:
        """Retorna o grau de saída (out-degree) do vértice ``u``.

        Raises:
            InvalidVertexError: Se ``u`` for inválido.
        """
        self._validateVertex(u)
        return len(self._adj[u])

    def _successors(self, u: int) -> Iterable[int]:
        """Retorna os vértices de destino das arestas que saem de ``u``.

        Raises:
            InvalidVertexError: Se ``u`` for inválido.
        """
        self._validateVertex(u)
        return list(self._adj[u].keys())
