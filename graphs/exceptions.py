"""Hierarquia de exceções customizadas para a biblioteca de grafos.

Cada exceção herda de ``GraphError`` (base própria da biblioteca) e também
de uma exceção built-in apropriada, permitindo que o código chamador capture
tanto a exceção específica da biblioteca quanto a exceção built-in padrão.
"""


class GraphError(Exception):
    """Classe base para todas as exceções da biblioteca de grafos."""


class InvalidVertexError(GraphError, IndexError):
    """Levantada quando um índice de vértice está fora do intervalo válido."""


class SelfLoopError(GraphError, ValueError):
    """Levantada ao tentar criar um laço (self-loop), proibido em grafos simples."""


class EdgeNotFoundError(GraphError, KeyError):
    """Levantada ao operar (ex.: ler peso) sobre uma aresta inexistente."""
