"""Camada de repositório: contrato e implementação do acesso a dados de Produto.

``IProdutoRepositorio`` é a interface de domínio: define *o que* o repositório
faz, sem expor SQL nem o driver do banco. O ``ProdutoService`` depende dessa
abstração (e não da classe concreta), o que permite trocar a fonte de dados —
banco real, mock em teste, outro SGBD — sem alterar a regra de negócio.

Este módulo lida apenas com SQL. A criptografia/descriptografia da descrição é
responsabilidade da camada de serviço.
"""

from abc import ABC, abstractmethod

import psycopg2.extensions

from src.domain.produto import Produto


class IProdutoRepositorio(ABC):
    """Contrato de persistência de produtos (interface de domínio)."""

    @abstractmethod
    def buscar_por_id(self, id_produto: int) -> Produto | None:
        ...

    @abstractmethod
    def listar_todos(self) -> list[Produto]:
        ...

    @abstractmethod
    def salvar(self, produto: Produto) -> None:
        ...

    @abstractmethod
    def atualizar(self, produto: Produto) -> None:
        ...

    @abstractmethod
    def excluir(self, id_produto: int) -> None:
        ...


class ProdutoRepositorio(IProdutoRepositorio):
    """Implementação PostgreSQL do repositório de produtos."""

    _COLUNAS = (
        "idProduto, nome, descricao, custoProduto, "
        "custofixo, comissao, imposto, margemLucro"
    )

    def __init__(self, connection: psycopg2.extensions.connection) -> None:
        self._connection = connection

    def buscar_por_id(self, id_produto: int) -> Produto | None:
        with self._connection.cursor() as cursor:
            cursor.execute(
                f"SELECT {self._COLUNAS} FROM produtos WHERE idProduto = %s",
                (id_produto,),
            )
            linha = cursor.fetchone()
        return self._linha_para_produto(linha) if linha else None

    def listar_todos(self) -> list[Produto]:
        with self._connection.cursor() as cursor:
            cursor.execute(
                f"SELECT {self._COLUNAS} FROM produtos ORDER BY idProduto"
            )
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
                    produto.descricao,
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
                    produto.descricao,
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
            descricao=linha[2],
            custo_produto=float(linha[3]),
            custo_fixo=float(linha[4]),
            comissao=float(linha[5]),
            imposto=float(linha[6]),
            margem_lucro=float(linha[7]),
        )
