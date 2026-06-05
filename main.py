"""Ponto de entrada da aplicação.

Responsabilidade única: compor as dependências e iniciar a CLI.
"""

import time

from src.data.connection import conectar_banco
from src.data.schema import criar_tabela
from src.presentation.cli import CLI
from src.service.produto_service import ProdutoRepositorio, ProdutoService


def main() -> None:
    conn = conectar_banco()
    criar_tabela(conn)

    repositorio = ProdutoRepositorio(conn)
    servico     = ProdutoService(repositorio)
    cli         = CLI(servico)

    time.sleep(1)
    cli.iniciar()

    conn.close()


if __name__ == "__main__":
    main()
