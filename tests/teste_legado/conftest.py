"""Configuração compartilhada dos testes do código legado.

O legado em ``pi_legado/`` não é um pacote Python (não tem ``__init__.py``
nem é instalável). Para que ``import funcoes`` funcione a partir dos testes,
adicionamos a pasta ``pi_legado`` ao ``sys.path`` aqui.
"""

import sys
from pathlib import Path

PI_LEGADO = Path(__file__).resolve().parents[2] / "pi_legado"
if str(PI_LEGADO) not in sys.path:
    sys.path.insert(0, str(PI_LEGADO))
