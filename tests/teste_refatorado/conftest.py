"""Configuração compartilhada dos testes do código refatorado.

Adiciona a raiz do projeto ao sys.path para que os imports
de src.* funcionem a partir dos testes.
"""

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))
