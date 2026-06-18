"""Representação de grafo por matriz de adjacência.

A classe :class:`AdjacencyMatrixGraph` armazena as arestas em uma matriz
``n x n``, onde cada posição guarda o peso da aresta correspondente (ou
``None`` quando a aresta não existe). Essa representação favorece consultas
de existência e peso de aresta em tempo O(1), em troca de espaço O(n^2) e de
um custo O(n) para calcular graus de vértice.
"""

from collections.abc import Iterable

from .abstract_graph import AbstractGraph
from .exceptions import EdgeNotFoundError, SelfLoopError


class AdjacencyMatrixGraph(AbstractGraph):
    """Grafo simples e direcionado representado por matriz de adjacência.

    As arestas são armazenadas em ``self._matrix``, uma matriz ``n x n`` de
    pesos (``float``) ou ``None`` quando a aresta correspondente não existe.
    A contagem de arestas é mantida incrementalmente em ``self._edgeCount``
    para que ``getEdgeCount`` seja O(1).
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
        self._matrix: list[list[float | None]] = [[None] * n for _ in range(n)]
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
        return self._matrix[u][v] is not None

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
        if self._matrix[u][v] is not None:
            return
        self._matrix[u][v] = self.DEFAULT_WEIGHT
        self._edgeCount += 1

    def removeEdge(self, u: int, v: int) -> None:
        """Remove a aresta ``u -> v``, se existir.

        Raises:
            InvalidVertexError: Se ``u`` ou ``v`` for inválido.
        """
        self._validateVertex(u)
        self._validateVertex(v)
        if self._matrix[u][v] is None:
            return
        self._matrix[u][v] = None
        self._edgeCount -= 1

    def setEdgeWeight(self, u: int, v: int, w: float) -> None:
        """Define o peso da aresta ``u -> v``.

        Raises:
            InvalidVertexError: Se ``u`` ou ``v`` for inválido.
            EdgeNotFoundError: Se a aresta ``u -> v`` não existir.
        """
        self._validateVertex(u)
        self._validateVertex(v)
        if self._matrix[u][v] is None:
            raise EdgeNotFoundError(f"Edge ({u}, {v}) not found")
        self._matrix[u][v] = w

    def getEdgeWeight(self, u: int, v: int) -> float:
        """Retorna o peso da aresta ``u -> v``.

        Raises:
            InvalidVertexError: Se ``u`` ou ``v`` for inválido.
            EdgeNotFoundError: Se a aresta ``u -> v`` não existir.
        """
        self._validateVertex(u)
        self._validateVertex(v)
        weight = self._matrix[u][v]
        if weight is None:
            raise EdgeNotFoundError(f"Edge ({u}, {v}) not found")
        return weight

    def getVertexInDegree(self, u: int) -> int:
        """Retorna o grau de entrada (in-degree) do vértice ``u``.

        Raises:
            InvalidVertexError: Se ``u`` for inválido.
        """
        self._validateVertex(u)
        return sum(1 for r in range(self._numVertices) if self._matrix[r][u] is not None)

    def getVertexOutDegree(self, u: int) -> int:
        """Retorna o grau de saída (out-degree) do vértice ``u``.

        Raises:
            InvalidVertexError: Se ``u`` for inválido.
        """
        self._validateVertex(u)
        return sum(1 for c in range(self._numVertices) if self._matrix[u][c] is not None)

    def _successors(self, u: int) -> Iterable[int]:
        """Retorna os vértices de destino das arestas que saem de ``u``.

        Raises:
            InvalidVertexError: Se ``u`` for inválido.
        """
        self._validateVertex(u)
        return [v for v in range(self._numVertices) if self._matrix[u][v] is not None]
