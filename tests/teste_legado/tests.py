import pytest
from pathlib import Path


# Comandos
# python -m pytest -v
# coverage: 
# python -m pytest --cov=. --cov-report=term-missing --cov-report=html


@pytest.fixture
def sis(tmp_path, monkeypatch):
    """Isola o banco em diretorio temporario por teste."""
    monkeypatch.chdir(tmp_path)
    s = Sis()
    yield s
    s.close()
    

@pytest.fixture
def pedEspecial(tmp_path, monkeypatch):
    """Isola o banco em diretorio temporario por teste."""
    monkeypatch.chdir(tmp_path)
    pe = PedEspecial()
    yield pe
    pe.close()

