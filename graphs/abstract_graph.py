"""Classe abstrata que define a API comum para grafos simples e direcionados.

A lógica compartilhada entre representações (ex.: matriz de adjacência e
lista de adjacência) fica concentrada em :class:`AbstractGraph`. As classes
concretas precisam apenas implementar os métodos abstratos declarados aqui,
incluindo o auxiliar protegido ``_successors``, usado pelos algoritmos
genéricos (como ``isConnected``) que são independentes de representação.
"""

import datetime
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from collections import deque
from collections.abc import Iterable

from .exceptions import InvalidVertexError


class AbstractGraph(ABC):
    """Define a API comum a todas as representações de grafo.

    Um grafo simples e direcionado não possui laços (self-loops) nem
    arestas múltiplas (multi-edges). Os vértices são índices inteiros no
    intervalo ``0 .. numVertices - 1``, fixados na construção.
    """

    DEFAULT_WEIGHT: float = 1.0

    def __init__(self, numVertices: int) -> None:
        """Inicializa o grafo com ``numVertices`` vértices e nenhuma aresta.

        Args:
            numVertices: Quantidade de vértices do grafo. Deve ser um
                inteiro maior ou igual a zero.

        Raises:
            ValueError: Se ``numVertices`` não for um ``int`` ou for
                negativo.
        """
        if not isinstance(numVertices, int) or isinstance(numVertices, bool):
            raise ValueError("numVertices deve ser um inteiro.")
        if numVertices < 0:
            raise ValueError("numVertices deve ser maior ou igual a zero.")

        self._numVertices = numVertices
        self._vertexWeights: list[float] = [self.DEFAULT_WEIGHT] * numVertices

    def _validateVertex(self, v: int) -> None:
        """Valida que ``v`` é um índice de vértice existente no grafo.

        Args:
            v: Índice de vértice a validar.

        Raises:
            InvalidVertexError: Se ``v`` estiver fora de
                ``[0, numVertices - 1]``.
        """
        if not 0 <= v < self._numVertices:
            raise InvalidVertexError(
                f"Vertex index {v} out of range [0, {self._numVertices - 1}]"
            )

    # ------------------------------------------------------------------
    # Métodos concretos compartilhados
    # ------------------------------------------------------------------

    def getVertexCount(self) -> int:
        """Retorna a quantidade de vértices do grafo."""
        return self._numVertices

    def setVertexWeight(self, v: int, w: float) -> None:
        """Define o peso do vértice ``v``.

        Args:
            v: Índice do vértice.
            w: Novo peso a atribuir.

        Raises:
            InvalidVertexError: Se ``v`` for inválido.
        """
        self._validateVertex(v)
        self._vertexWeights[v] = w

    def getVertexWeight(self, v: int) -> float:
        """Retorna o peso do vértice ``v``.

        Args:
            v: Índice do vértice.

        Raises:
            InvalidVertexError: Se ``v`` for inválido.
        """
        self._validateVertex(v)
        return self._vertexWeights[v]

    def isSuccessor(self, u: int, v: int) -> bool:
        """Verifica se ``v`` é sucessor de ``u`` (existe aresta ``u -> v``)."""
        return self.hasEdge(u, v)

    def isPredecessor(self, u: int, v: int) -> bool:
        """Verifica se ``u`` é predecessor de ``v`` (existe aresta ``u -> v``)."""
        return self.hasEdge(u, v)

    def isDivergent(self, u1: int, v1: int, u2: int, v2: int) -> bool:
        """Verifica se as arestas ``(u1, v1)`` e ``(u2, v2)`` são divergentes.

        Duas arestas são divergentes quando compartilham a mesma origem e
        são distintas entre si. Trata-se de um predicado estrutural: não é
        necessário que as arestas existam de fato no grafo.

        Raises:
            InvalidVertexError: Se algum dos quatro índices for inválido.
        """
        self._validateVertex(u1)
        self._validateVertex(v1)
        self._validateVertex(u2)
        self._validateVertex(v2)
        return u1 == u2 and v1 != v2

    def isConvergent(self, u1: int, v1: int, u2: int, v2: int) -> bool:
        """Verifica se as arestas ``(u1, v1)`` e ``(u2, v2)`` são convergentes.

        Duas arestas são convergentes quando compartilham o mesmo destino e
        são distintas entre si. Trata-se de um predicado estrutural: não é
        necessário que as arestas existam de fato no grafo.

        Raises:
            InvalidVertexError: Se algum dos quatro índices for inválido.
        """
        self._validateVertex(u1)
        self._validateVertex(v1)
        self._validateVertex(u2)
        self._validateVertex(v2)
        return v1 == v2 and u1 != u2

    def isIncident(self, u: int, v: int, x: int) -> bool:
        """Verifica se o vértice ``x`` é incidente à aresta ``(u, v)``.

        Trata-se de um predicado estrutural: não é necessário que a aresta
        ``(u, v)`` exista de fato no grafo.

        Raises:
            InvalidVertexError: Se ``u``, ``v`` ou ``x`` for inválido.
        """
        self._validateVertex(u)
        self._validateVertex(v)
        self._validateVertex(x)
        return x == u or x == v

    def isEmptyGraph(self) -> bool:
        """Verifica se o grafo não possui nenhuma aresta."""
        return self.getEdgeCount() == 0

    def isCompleteGraph(self) -> bool:
        """Verifica se o grafo possui todas as arestas possíveis.

        Para um grafo simples e direcionado com ``n`` vértices (sem laços),
        o número máximo de arestas é ``n * (n - 1)``.
        """
        n = self._numVertices
        return self.getEdgeCount() == n * (n - 1)

    def isConnected(self, strong: bool = False) -> bool:
        """Verifica se o grafo é conectado.

        Args:
            strong: Se ``False`` (padrão), verifica conectividade fraca
                (weakly connected), tratando as arestas como não
                direcionadas. Se ``True``, verifica conectividade forte
                (strongly connected), exigindo que todo vértice seja
                alcançável a partir do vértice ``0`` e que o vértice ``0``
                seja alcançável a partir de todo vértice (considerando o
                sentido das arestas).

        Returns:
            ``True`` se o grafo satisfizer o critério de conectividade
            escolhido; ``False`` caso contrário.
        """
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
            visited = bfs(0, undirected)
            return len(visited) == n

        reached_forward = bfs(0, forward)
        reached_backward = bfs(0, reverse)
        return len(reached_forward) == n and len(reached_backward) == n

    def exportToGEPHI(self, path: str) -> None:
        """Exporta o grafo para um arquivo GEXF 1.2 legível pelo Gephi.

        O arquivo gerado contém todos os vértices e arestas do grafo. O
        peso de cada vértice é exportado como um atributo customizado de
        nó (``id="0"``, ``title="weight"``) e o peso de cada aresta é
        exportado através do atributo nativo ``weight`` do GEXF. O método
        usa apenas a API pública (``getVertexCount``, ``getVertexWeight``,
        ``getEdgeWeight``) e o auxiliar protegido ``_successors``, sendo
        portanto independente da representação interna escolhida pela
        classe concreta.

        Args:
            path: Caminho do arquivo de destino. Deve terminar com a
                extensão ``.gexf`` (case-insensitive).

        Raises:
            ValueError: Se ``path`` não terminar com a extensão ``.gexf``.
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

    # ------------------------------------------------------------------
    # Métodos abstratos — implementados pelas classes concretas
    # ------------------------------------------------------------------

    @abstractmethod
    def getEdgeCount(self) -> int:
        """Retorna a quantidade de arestas do grafo."""
        raise NotImplementedError

    @abstractmethod
    def hasEdge(self, u: int, v: int) -> bool:
        """Verifica se existe aresta direcionada de ``u`` para ``v``."""
        raise NotImplementedError

    @abstractmethod
    def addEdge(self, u: int, v: int) -> None:
        """Adiciona a aresta direcionada ``u -> v``.

        A operação é idempotente: chamadas repetidas com o mesmo par
        ``(u, v)`` não criam arestas duplicadas nem alteram a contagem de
        arestas. Laços (``u == v``) são proibidos.

        Raises:
            InvalidVertexError: Se ``u`` ou ``v`` for inválido.
            SelfLoopError: Se ``u == v``.
        """
        raise NotImplementedError

    @abstractmethod
    def removeEdge(self, u: int, v: int) -> None:
        """Remove a aresta ``u -> v``, se existir."""
        raise NotImplementedError

    @abstractmethod
    def getVertexInDegree(self, u: int) -> int:
        """Retorna o grau de entrada (in-degree) do vértice ``u``."""
        raise NotImplementedError

    @abstractmethod
    def getVertexOutDegree(self, u: int) -> int:
        """Retorna o grau de saída (out-degree) do vértice ``u``."""
        raise NotImplementedError

    @abstractmethod
    def setEdgeWeight(self, u: int, v: int, w: float) -> None:
        """Define o peso da aresta ``u -> v``.

        Raises:
            EdgeNotFoundError: Se a aresta ``u -> v`` não existir.
        """
        raise NotImplementedError

    @abstractmethod
    def getEdgeWeight(self, u: int, v: int) -> float:
        """Retorna o peso da aresta ``u -> v``.

        Raises:
            EdgeNotFoundError: Se a aresta ``u -> v`` não existir.
        """
        raise NotImplementedError

    @abstractmethod
    def _successors(self, u: int) -> Iterable[int]:
        """Retorna os vértices de destino das arestas que saem de ``u``.

        Método protegido, usado pelos algoritmos genéricos definidos em
        ``AbstractGraph`` (ex.: ``isConnected``) de forma independente da
        representação interna escolhida pela classe concreta.
        """
        raise NotImplementedError
