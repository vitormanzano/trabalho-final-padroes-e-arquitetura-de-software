# Criação do schema (DDL) do banco de dados.
# Mantido separado da conexão: este módulo cuida apenas da estrutura
# das tabelas.

_CREATE_PRODUTOS = """
    CREATE TABLE Produtos (
        idProduto INT PRIMARY KEY,
        nome VARCHAR2(255),
        descricao VARCHAR2(255),
        custoProduto DECIMAL(12, 2),
        custofixo DECIMAL(12, 2),
        comissao DECIMAL(12, 2),
        imposto DECIMAL(12, 2),
        margemLucro DECIMAL(12, 2)
    )
"""


def tabela_existe(connection, nome_tabela):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM user_tables WHERE table_name = :nome",
            nome=nome_tabela.upper(),
        )
        return cursor.fetchone() is not None


def criar_tabela(connection):
    if tabela_existe(connection, "Produtos"):
        return False
    with connection.cursor() as cursor:
        cursor.execute(_CREATE_PRODUTOS)
    connection.commit()
    return True
