_CREATE_PRODUTOS = """
    CREATE TABLE Produtos (
        idProduto INT PRIMARY KEY,
        nome VARCHAR(255),
        descricao VARCHAR(255),
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
            "SELECT 1 FROM information_schema.tables WHERE table_name = %s",
            (nome_tabela.lower(),),
        )
        return cursor.fetchone() is not None


def criar_tabela(connection):
    if tabela_existe(connection, "Produtos"):
        return False
    with connection.cursor() as cursor:
        cursor.execute(_CREATE_PRODUTOS)
    connection.commit()
    return True
