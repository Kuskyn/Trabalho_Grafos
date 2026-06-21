"""Representação de grafo por lista de adjacência."""

from collections.abc import Iterable

from .abstract_graph import AbstractGraph
from .exceptions import EdgeNotFoundError, SelfLoopError


class AdjacencyListGraph(AbstractGraph):
    """Grafo simples e direcionado armazenado em listas de adjacência.

    ``_adj`` mapeia, por vértice, ``destino -> peso``. ``_pred`` guarda os
    predecessores de cada vértice para que o grau de entrada seja O(1).
    """

    def __init__(self, numVertices: int) -> None:
        super().__init__(numVertices)
        n = self._numVertices
        self._adj: list[dict[int, float]] = [{} for _ in range(n)]
        self._pred: list[set[int]] = [set() for _ in range(n)]
        self._edgeCount: int = 0

    def getEdgeCount(self) -> int:
        return self._edgeCount

    def hasEdge(self, u: int, v: int) -> bool:
        self._validateVertex(u)
        self._validateVertex(v)
        return v in self._adj[u]

    def addEdge(self, u: int, v: int) -> None:
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
        self._validateVertex(u)
        self._validateVertex(v)
        if v not in self._adj[u]:
            return
        del self._adj[u][v]
        self._pred[v].discard(u)
        self._edgeCount -= 1

    def setEdgeWeight(self, u: int, v: int, w: float) -> None:
        self._validateVertex(u)
        self._validateVertex(v)
        if v not in self._adj[u]:
            raise EdgeNotFoundError(f"Edge ({u}, {v}) not found")
        self._adj[u][v] = w

    def getEdgeWeight(self, u: int, v: int) -> float:
        self._validateVertex(u)
        self._validateVertex(v)
        if v not in self._adj[u]:
            raise EdgeNotFoundError(f"Edge ({u}, {v}) not found")
        return self._adj[u][v]

    def getVertexInDegree(self, u: int) -> int:
        self._validateVertex(u)
        return len(self._pred[u])

    def getVertexOutDegree(self, u: int) -> int:
        self._validateVertex(u)
        return len(self._adj[u])

    def _successors(self, u: int) -> Iterable[int]:
        self._validateVertex(u)
        return list(self._adj[u].keys())
