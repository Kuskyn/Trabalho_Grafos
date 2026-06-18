"""Biblioteca de grafos simples e direcionados.

Etapa atual: classe abstrata, hierarquia de exceções e representações por
matriz de adjacência e por lista de adjacência.
"""

from .abstract_graph import AbstractGraph
from .adjacency_list_graph import AdjacencyListGraph
from .adjacency_matrix_graph import AdjacencyMatrixGraph
from .exceptions import GraphError, InvalidVertexError, SelfLoopError, EdgeNotFoundError

__all__ = [
    "AbstractGraph",
    "AdjacencyListGraph",
    "AdjacencyMatrixGraph",
    "GraphError",
    "InvalidVertexError",
    "SelfLoopError",
    "EdgeNotFoundError",
]
