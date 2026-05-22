# Configuração centralizada de acesso ao banco de dados.

import os
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[2]


def _carregar_env() -> None:
    """Carrega pares ``CHAVE=VALOR`` de um ``.env`` na raiz, se existir.

    Implementação mínima e sem dependências externas (dispensa o
    python-dotenv). Não sobrescreve variáveis de ambiente já definidas.
    """
    env_path = _RAIZ / ".env"
    if not env_path.exists():
        return
    for linha in env_path.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, _, valor = linha.partition("=")
        os.environ.setdefault(chave.strip(), valor.strip())


_carregar_env()


class Settings:
    """Parâmetros de conexão com o Oracle.

    As credenciais ficam em branco por padrão: precisam ser informadas
    por variáveis de ambiente ou pelo arquivo ``.env`` na raiz do projeto.
    """

    DB_USER: str = os.getenv("DB_USER", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_DSN: str = os.getenv("DB_DSN", "")


settings = Settings()
