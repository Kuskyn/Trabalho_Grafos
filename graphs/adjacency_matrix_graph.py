"""Representação de grafo por matriz de adjacência."""

from collections.abc import Iterable

from .abstract_graph import AbstractGraph
from .exceptions import EdgeNotFoundError, SelfLoopError


class AdjacencyMatrixGraph(AbstractGraph):
    """Grafo simples e direcionado armazenado em uma matriz ``n x n``.

    Cada posição guarda o peso da aresta ou ``None`` quando ela não existe.
    """

    def __init__(self, numVertices: int) -> None:
        super().__init__(numVertices)
        n = self._numVertices
        self._matrix: list[list[float | None]] = [[None] * n for _ in range(n)]
        self._edgeCount: int = 0

    def getEdgeCount(self) -> int:
        return self._edgeCount

    def hasEdge(self, u: int, v: int) -> bool:
        self._validateVertex(u)
        self._validateVertex(v)
        return self._matrix[u][v] is not None

    def addEdge(self, u: int, v: int) -> None:
        self._validateVertex(u)
        self._validateVertex(v)
        if u == v:
            raise SelfLoopError(f"Self-loops are not allowed (vertex {u})")
        if self._matrix[u][v] is not None:
            return
        self._matrix[u][v] = self.DEFAULT_WEIGHT
        self._edgeCount += 1

    def removeEdge(self, u: int, v: int) -> None:
        self._validateVertex(u)
        self._validateVertex(v)
        if self._matrix[u][v] is None:
            return
        self._matrix[u][v] = None
        self._edgeCount -= 1

    def setEdgeWeight(self, u: int, v: int, w: float) -> None:
        self._validateVertex(u)
        self._validateVertex(v)
        if self._matrix[u][v] is None:
            raise EdgeNotFoundError(f"Edge ({u}, {v}) not found")
        self._matrix[u][v] = w

    def getEdgeWeight(self, u: int, v: int) -> float:
        self._validateVertex(u)
        self._validateVertex(v)
        weight = self._matrix[u][v]
        if weight is None:
            raise EdgeNotFoundError(f"Edge ({u}, {v}) not found")
        return weight

    def getVertexInDegree(self, u: int) -> int:
        self._validateVertex(u)
        return sum(1 for r in range(self._numVertices) if self._matrix[r][u] is not None)

    def getVertexOutDegree(self, u: int) -> int:
        self._validateVertex(u)
        return sum(1 for c in range(self._numVertices) if self._matrix[u][c] is not None)

    def _successors(self, u: int) -> Iterable[int]:
        self._validateVertex(u)
        return [v for v in range(self._numVertices) if self._matrix[u][v] is not None]
