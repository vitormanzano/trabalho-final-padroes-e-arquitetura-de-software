"""Padrão Factory Method aplicado à criação do service de produtos.
"""

from abc import ABC, abstractmethod

from src.domain.strategy_preco import PrecoPorMarkup
from src.factory.repository_factory import PostgresRepositoryCreator
from src.service.produto_service import ProdutoService


class ServiceCreator(ABC):
    """Criador: declara o método fábrica que produz um ``ProdutoService``."""

    @abstractmethod
    def criar_service(self) -> ProdutoService:
        """Método fábrica: as subclasses decidem como compor o service."""
        ...


class PostgresServiceCreator(ServiceCreator):
    """Criador Concreto: fabrica o service apoiado no repositório PostgreSQL."""

    def criar_service(self) -> ProdutoService:
        repository = PostgresRepositoryCreator().criar_repository()
        # Estratégia de precificação injetada aqui: trocar a forma de precificar
        # é mudar esta linha — o ProdutoService não muda (padrão Strategy).
        return ProdutoService(repository, PrecoPorMarkup())
