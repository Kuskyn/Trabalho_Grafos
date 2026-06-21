"""Exceções da biblioteca de grafos."""


class GraphError(Exception):
    """Classe base para as exceções da biblioteca."""


class InvalidVertexError(GraphError, IndexError):
    """Índice de vértice fora do intervalo válido."""


class SelfLoopError(GraphError, ValueError):
    """Tentativa de criar um laço (proibido em grafos simples)."""


class EdgeNotFoundError(GraphError, KeyError):
    """Operação sobre uma aresta inexistente."""
