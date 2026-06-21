"""Classe abstrata com a API comum dos grafos simples e direcionados."""

import datetime
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from collections import deque
from collections.abc import Iterable

from .exceptions import InvalidVertexError


class AbstractGraph(ABC):
    """API comum às representações de grafo.

    Grafo simples e direcionado: sem laços e sem arestas múltiplas. Os
    vértices são índices inteiros em ``0 .. numVertices - 1``.
    """

    DEFAULT_WEIGHT: float = 1.0

    def __init__(self, numVertices: int) -> None:
        # bool é subclasse de int em Python, mas não é um nº de vértices válido.
        if not isinstance(numVertices, int) or isinstance(numVertices, bool):
            raise ValueError("numVertices deve ser um inteiro.")
        if numVertices < 0:
            raise ValueError("numVertices deve ser maior ou igual a zero.")

        self._numVertices = numVertices
        self._vertexWeights: list[float] = [self.DEFAULT_WEIGHT] * numVertices

    def _validateVertex(self, v: int) -> None:
        if not 0 <= v < self._numVertices:
            raise InvalidVertexError(
                f"Vertex index {v} out of range [0, {self._numVertices - 1}]"
            )

    def getVertexCount(self) -> int:
        return self._numVertices

    def setVertexWeight(self, v: int, w: float) -> None:
        self._validateVertex(v)
        self._vertexWeights[v] = w

    def getVertexWeight(self, v: int) -> float:
        self._validateVertex(v)
        return self._vertexWeights[v]

    def isSuccessor(self, u: int, v: int) -> bool:
        """``v`` é sucessor de ``u`` se existe a aresta ``u -> v``."""
        return self.hasEdge(u, v)

    def isPredecessor(self, u: int, v: int) -> bool:
        """``u`` é predecessor de ``v`` se existe a aresta ``u -> v``."""
        return self.hasEdge(u, v)

    def isDivergent(self, u1: int, v1: int, u2: int, v2: int) -> bool:
        """Arestas distintas com a mesma origem."""
        self._validateVertex(u1)
        self._validateVertex(v1)
        self._validateVertex(u2)
        self._validateVertex(v2)
        return u1 == u2 and v1 != v2

    def isConvergent(self, u1: int, v1: int, u2: int, v2: int) -> bool:
        """Arestas distintas com o mesmo destino."""
        self._validateVertex(u1)
        self._validateVertex(v1)
        self._validateVertex(u2)
        self._validateVertex(v2)
        return v1 == v2 and u1 != u2

    def isIncident(self, u: int, v: int, x: int) -> bool:
        """``x`` é incidente à aresta ``(u, v)``."""
        self._validateVertex(u)
        self._validateVertex(v)
        self._validateVertex(x)
        return x == u or x == v

    def isEmptyGraph(self) -> bool:
        return self.getEdgeCount() == 0

    def isCompleteGraph(self) -> bool:
        # Máximo de arestas de um grafo simples direcionado sem laços: n*(n-1).
        n = self._numVertices
        return self.getEdgeCount() == n * (n - 1)

    def isConnected(self, strong: bool = False) -> bool:
        """Verifica conectividade fraca (padrão) ou forte (``strong=True``)."""
        n = self._numVertices
        if n <= 1:
            return True

        forward: list[list[int]] = [[] for _ in range(n)]
        reverse: list[list[int]] = [[] for _ in range(n)]
        for u in range(n):
            for v in self._successors(u):
                forward[u].append(v)
                reverse[v].append(u)

        def bfs(start: int, adjacency: list[list[int]]) -> set[int]:
            visited = {start}
            queue: deque[int] = deque([start])
            while queue:
                current = queue.popleft()
                for neighbor in adjacency[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            return visited

        if not strong:
            undirected: list[list[int]] = [
                forward[i] + reverse[i] for i in range(n)
            ]
            return len(bfs(0, undirected)) == n

        reached_forward = bfs(0, forward)
        reached_backward = bfs(0, reverse)
        return len(reached_forward) == n and len(reached_backward) == n

    def exportToGEPHI(self, path: str) -> None:
        """Exporta o grafo para um arquivo GEXF 1.2 legível pelo Gephi.

        Usa apenas a API pública e ``_successors``, sendo independente da
        representação interna. O peso do vértice vira um atributo de nó e o
        peso da aresta usa o atributo nativo ``weight`` do GEXF.
        """
        if not path.lower().endswith(".gexf"):
            raise ValueError(
                f"path deve terminar com a extensão '.gexf', recebido: {path!r}"
            )

        root = ET.Element(
            "gexf",
            {"xmlns": "http://www.gexf.net/1.2draft", "version": "1.2"},
        )

        meta = ET.SubElement(
            root, "meta", {"lastmodifieddate": datetime.date.today().isoformat()}
        )
        creator = ET.SubElement(meta, "creator")
        creator.text = "graphs"
        description = ET.SubElement(meta, "description")
        description.text = "Simple directed graph"

        graph = ET.SubElement(
            root, "graph", {"mode": "static", "defaultedgetype": "directed"}
        )

        attributes = ET.SubElement(graph, "attributes", {"class": "node"})
        ET.SubElement(
            attributes, "attribute", {"id": "0", "title": "weight", "type": "double"}
        )

        nodes = ET.SubElement(graph, "nodes")
        for i in range(self.getVertexCount()):
            node = ET.SubElement(nodes, "node", {"id": str(i), "label": str(i)})
            attvalues = ET.SubElement(node, "attvalues")
            ET.SubElement(
                attvalues,
                "attvalue",
                {"for": "0", "value": str(self.getVertexWeight(i))},
            )

        edges = ET.SubElement(graph, "edges")
        k = 0
        for u in range(self.getVertexCount()):
            for v in self._successors(u):
                ET.SubElement(
                    edges,
                    "edge",
                    {
                        "id": str(k),
                        "source": str(u),
                        "target": str(v),
                        "weight": str(self.getEdgeWeight(u, v)),
                    },
                )
                k += 1

        tree = ET.ElementTree(root)
        ET.indent(tree)
        tree.write(path, encoding="utf-8", xml_declaration=True)

    @abstractmethod
    def getEdgeCount(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def hasEdge(self, u: int, v: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def addEdge(self, u: int, v: int) -> None:
        """Adiciona a aresta ``u -> v``. Idempotente; proíbe laços."""
        raise NotImplementedError

    @abstractmethod
    def removeEdge(self, u: int, v: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def getVertexInDegree(self, u: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def getVertexOutDegree(self, u: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def setEdgeWeight(self, u: int, v: int, w: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def getEdgeWeight(self, u: int, v: int) -> float:
        raise NotImplementedError

    @abstractmethod
    def _successors(self, u: int) -> Iterable[int]:
        """Vértices de destino das arestas que saem de ``u``."""
        raise NotImplementedError
