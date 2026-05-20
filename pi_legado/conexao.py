# python -m pip install oracledb 
import oracledb
import getpass


# Teste de Conexão


def conectar_banco():
    connection = oracledb.connect(
        user = "system",
        password = 'Oracle123',
        dsn = "localhost/xe")
    return connection

def tabela_existe(connection, nome_tabela):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM {}".format(nome_tabela))
        return True
    except oracledb.DatabaseError as erro:
        return False
    
def criar_tabela(connection):
    cursor = connection.cursor()
    if not tabela_existe(connection, 'PIprodutos'):
        cursor.execute("""
                CREATE TABLE PIProdutos (
                    idProduto INT PRIMARY KEY,
                    nome VARCHAR2(255),
                    descricao VARCHAR2(255),
                    custoProduto DECIMAL(12, 2),
                    custofixo DECIMAL(12, 2),
                    comissao DECIMAL(12, 2),
                    imposto DECIMAL(12, 2),
                    margemLucro DECIMAL(12, 2)
                )""")
        connection.commit()
        cursor.close()
    else:
        None

    
conexao = conectar_banco()

if conexao:
    criar_tabela(conexao)
    conexao.close()


