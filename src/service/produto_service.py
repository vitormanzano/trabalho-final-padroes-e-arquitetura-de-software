"""Camada de serviço: regras de negócio e coordenação com a persistência.

Não conhece detalhes de terminal nem de SQL. Depende da interface
``IProdutoRepositorio`` (e não da implementação concreta), de modo que a
persistência pode ser trocada sem alterar a regra de negócio.

A criptografia da descrição é responsabilidade desta camada: o serviço cifra
antes de persistir e decifra ao recuperar, mantendo o repositório alheio à
cifra e os objetos ``Produto`` devolvidos ao chamador sempre em texto claro.
"""

from dataclasses import replace

from src.domain.cifra import criptografar, descriptografar
from src.domain.produto import Produto
from src.domain.validacao import validar_produto
from src.repository.produto_repository import IProdutoRepositorio, ProdutoRepositorio

__all__ = ["ProdutoRepositorio", "ProdutoService"]


class ProdutoService:
    """Orquestra validação, domínio, cifra e persistência."""

    def __init__(self, repositorio: IProdutoRepositorio) -> None:
        self._repositorio = repositorio

    def buscar_produto(self, id_produto: int) -> Produto | None:
        produto = self._repositorio.buscar_por_id(id_produto)
        return self._decifrar(produto) if produto else None

    def listar_produtos(self) -> list[Produto]:
        return [self._decifrar(p) for p in self._repositorio.listar_todos()]

    def cadastrar_produto(
        self,
        id_produto: int,
        nome: str,
        descricao: str,
        custo_produto: float,
        custo_fixo: float,
        comissao: float,
        imposto: float,
        margem_lucro: float,
    ) -> Produto:
        validar_produto(
            id_produto, nome, descricao,
            custo_produto, custo_fixo, comissao, imposto, margem_lucro,
        )
        if self._repositorio.buscar_por_id(id_produto) is not None:
            raise ValueError(f"Produto com id {id_produto} já existe.")
        produto = Produto(
            id_produto=id_produto,
            nome=nome,
            descricao=descricao,
            custo_produto=custo_produto,
            custo_fixo=custo_fixo,
            comissao=comissao,
            imposto=imposto,
            margem_lucro=margem_lucro,
        )
        self._repositorio.salvar(self._cifrar(produto))
        return produto

    def atualizar_produto(self, produto: Produto) -> None:
        validar_produto(
            produto.id_produto, produto.nome, produto.descricao,
            produto.custo_produto, produto.custo_fixo,
            produto.comissao, produto.imposto, produto.margem_lucro,
        )
        self._repositorio.atualizar(self._cifrar(produto))

    def excluir_produto(self, id_produto: int) -> None:
        if self._repositorio.buscar_por_id(id_produto) is None:
            raise ValueError(f"Produto com id {id_produto} não encontrado.")
        self._repositorio.excluir(id_produto)

    @staticmethod
    def _cifrar(produto: Produto) -> Produto:
        return replace(produto, descricao=criptografar(produto.descricao))

    @staticmethod
    def _decifrar(produto: Produto) -> Produto:
        return replace(produto, descricao=descriptografar(produto.descricao))
