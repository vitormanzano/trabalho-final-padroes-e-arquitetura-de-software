"""Camada de serviço: regras de negócio e coordenação com a persistência.

Não conhece detalhes de terminal nem de SQL.
Depende diretamente do ProdutoRepositorio concreto — sem interface ainda.
"""

import psycopg

from src.domain.cifra import criptografar, descriptografar
from src.domain.produto import Produto
from src.domain.validacao import ErroValidacao, validar_produto


class ProdutoRepositorio:
    """Acesso a dados de produto: traduz operações de domínio em SQL."""

    def __init__(self, connection: psycopg.Connection) -> None:
        self._connection = connection

    def buscar_por_id(self, id_produto: int) -> Produto | None:
        with self._connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM produtos WHERE idProduto = %s",
                (id_produto,),
            )
            linha = cursor.fetchone()
        return self._linha_para_produto(linha) if linha else None

    def listar_todos(self) -> list[Produto]:
        with self._connection.cursor() as cursor:
            cursor.execute("SELECT * FROM produtos ORDER BY idProduto")
            linhas = cursor.fetchall()
        return [self._linha_para_produto(linha) for linha in linhas]

    def salvar(self, produto: Produto) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO produtos
                    (idProduto, nome, descricao, custoProduto,
                     custofixo, comissao, imposto, margemLucro)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    produto.id_produto,
                    produto.nome,
                    criptografar(produto.descricao),
                    produto.custo_produto,
                    produto.custo_fixo,
                    produto.comissao,
                    produto.imposto,
                    produto.margem_lucro,
                ),
            )
        self._connection.commit()

    def atualizar(self, produto: Produto) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE produtos SET
                    nome         = %s,
                    descricao    = %s,
                    custoProduto = %s,
                    custofixo    = %s,
                    comissao     = %s,
                    imposto      = %s,
                    margemLucro  = %s
                WHERE idProduto = %s
                """,
                (
                    produto.nome,
                    criptografar(produto.descricao),
                    produto.custo_produto,
                    produto.custo_fixo,
                    produto.comissao,
                    produto.imposto,
                    produto.margem_lucro,
                    produto.id_produto,
                ),
            )
        self._connection.commit()

    def excluir(self, id_produto: int) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM produtos WHERE idProduto = %s",
                (id_produto,),
            )
        self._connection.commit()

    @staticmethod
    def _linha_para_produto(linha: tuple) -> Produto:
        return Produto(
            id_produto=linha[0],
            nome=linha[1],
            descricao=descriptografar(linha[2]),
            custo_produto=float(linha[3]),
            custo_fixo=float(linha[4]),
            comissao=float(linha[5]),
            imposto=float(linha[6]),
            margem_lucro=float(linha[7]),
        )


class ProdutoService:
    """Orquestra validação, domínio e persistência."""

    def __init__(self, repositorio: ProdutoRepositorio) -> None:
        self._repositorio = repositorio

    def buscar_produto(self, id_produto: int) -> Produto | None:
        return self._repositorio.buscar_por_id(id_produto)

    def listar_produtos(self) -> list[Produto]:
        return self._repositorio.listar_todos()

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
        self._repositorio.salvar(produto)
        return produto

    def atualizar_produto(self, produto: Produto) -> None:
        validar_produto(
            produto.id_produto, produto.nome, produto.descricao,
            produto.custo_produto, produto.custo_fixo,
            produto.comissao, produto.imposto, produto.margem_lucro,
        )
        self._repositorio.atualizar(produto)

    def excluir_produto(self, id_produto: int) -> None:
        if self._repositorio.buscar_por_id(id_produto) is None:
            raise ValueError(f"Produto com id {id_produto} não encontrado.")
        self._repositorio.excluir(id_produto)
