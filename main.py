"""Ponto de entrada da aplicação.

Responsabilidade única: compor as dependências e iniciar a CLI.
"""

import time

from src.data.connection import conectar_banco
from src.data.schema import criar_tabela
from src.factory.service_factory import PostgresServiceCreator
from src.presentation.cli import CLI


def main() -> None:
    conn = conectar_banco()
    criar_tabela(conn)

    # Factory Method: o Criador fabrica o service já composto com seu
    # repositório. O cliente não conhece a fonte de dados por trás.
    servico = PostgresServiceCreator().criar_service()
    cli     = CLI(servico)

    time.sleep(1)
    cli.iniciar()

    conn.close()


if __name__ == "__main__":
    main()
