"""Padrão Factory Method aplicado à criação do repositório de produtos.
"""

from abc import ABC, abstractmethod

from src.data.connection import conectar_banco
from src.repository.produto_repository import IProdutoRepository, ProdutoRepository


class RepositoryCreator(ABC):
    """Criador: declara o método fábrica que produz um ``IProdutoRepository``."""

    @abstractmethod
    def criar_repository(self) -> IProdutoRepository:
        """Método fábrica: as subclasses decidem qual repositório instanciar."""
        ...


class PostgresRepositoryCreator(RepositoryCreator):
    """Criador Concreto: fabrica o repositório apoiado em PostgreSQL."""

    def criar_repository(self) -> IProdutoRepository:
        return ProdutoRepository(conectar_banco())
