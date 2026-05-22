"""Testes de caracterização para ``pi_legado/funcoes.py``.

após a refatoração, esses testes devem seguir com a mesma entrada e saída correspondente.

Cobertura:
- ``criptografia``    — cifra de substituição usada no cadastro.
- ``descriptografia`` — operação inversa, usada na listagem.
- ``mostrar_dados``   — formatação/impressão de um produto.
- ``funcmenu``        — leitura da opção do menu.

Como rodar:
    python -m pytest -v
    python -m pytest --cov=pi_legado --cov-report=term-missing
"""

import pytest

from funcoes import criptografia, descriptografia, funcmenu, mostrar_dados


# --------------------------------------------------------------------------
# criptografia
# --------------------------------------------------------------------------

@pytest.mark.parametrize("texto, esperado", [
    ("OI", "IG"),
    ("BANANA", "KDGPGP"),
    ("CASA", "OEAU"),
])
def test_criptografia_valores_conhecidos(texto, esperado):
    """Valores de referência (golden values) extraídos do código atual."""
    assert criptografia(texto) == esperado


def test_criptografia_ignora_caixa():
    """O texto é convertido para maiúsculas antes de cifrar."""
    assert criptografia("casa") == criptografia("CASA")


def test_criptografia_remove_espacos():
    """Espaços são descartados antes de cifrar."""
    assert criptografia("A B C D") == criptografia("ABCD")


def test_criptografia_texto_impar_duplica_ultima_letra():
    """Texto de comprimento ímpar recebe padding: a última letra é repetida.

    Por isso ``criptografia("A")`` é igual a ``criptografia("AA")``.
    """
    assert criptografia("A") == criptografia("AA")


def test_criptografia_string_vazia_retorna_vazia():
    assert criptografia("") == ""


def test_criptografia_rejeita_caractere_fora_do_alfabeto():
    """Dígitos e acentos não estão na tabela A–Z e quebram a função."""
    with pytest.raises(ValueError):
        criptografia("TESTE1")


# --------------------------------------------------------------------------
# descriptografia
# --------------------------------------------------------------------------

@pytest.mark.parametrize("texto", ["OI", "BANANA", "CASA", "FEIJAO"])
def test_roundtrip_texto_par(texto):
    """Texto de comprimento par volta ao original após cifrar e decifrar."""
    assert descriptografia(criptografia(texto)) == texto


def test_roundtrip_texto_impar_mantem_padding():
    """Texto de comprimento ímpar NÃO volta idêntico.

    O padding da criptografia duplica a última letra, então
    ``"TESTE"`` reaparece como ``"TESTEE"`` após o roundtrip.
    """
    assert descriptografia(criptografia("TESTE")) == "TESTEE"


# --------------------------------------------------------------------------
# mostrar_dados
# --------------------------------------------------------------------------

def _linha_produto(margem_lucro, descricao="FEIJAO"):
    """Monta uma linha no formato que ``mostrar_dados`` espera (row[0..7]).

    A descrição é armazenada cifrada no "banco", pois ``mostrar_dados``
    aplica ``descriptografia`` sobre ela.
    """
    return (
        1,                        # row[0] idProduto
        "Arroz",                  # row[1] nome
        criptografia(descricao),  # row[2] descricao (cifrada)
        100.0,                    # row[3] custoProduto
        10.0,                     # row[4] custofixo
        5.0,                      # row[5] comissao
        8.0,                      # row[6] imposto
        margem_lucro,             # row[7] margemLucro
    )


def test_mostrar_dados_imprime_nome_e_descricao(capsys):
    """A linha impressa contém o nome e a descrição já decifrada."""
    mostrar_dados([_linha_produto(25.0)])
    saida = capsys.readouterr().out
    assert "Arroz" in saida
    assert "FEIJAO" in saida
    assert "Preço de venda" in saida


@pytest.mark.parametrize("margem, rotulo", [
    (25.0, "Margem de lucro alta"),
    (15.0, "Margem de lucro média"),
    (5.0, "Margem de lucro baixa"),
    (0.0, "Equilíbrio"),
    (-5.0, "Prejuízo"),
])
def test_mostrar_dados_classifica_rentabilidade(capsys, margem, rotulo):
    """Cada faixa de margem de lucro gera um rótulo de rentabilidade."""
    mostrar_dados([_linha_produto(margem)])
    assert rotulo in capsys.readouterr().out


def test_mostrar_dados_divisao_por_zero_quando_porcentagens_somam_100():
    """Defeito conhecido: custo fixo + comissão + imposto + margem = 100
    zera o denominador do preço de venda e estoura ZeroDivisionError.
    """
    linha = (1, "Arroz", criptografia("FEIJAO"), 100.0, 25.0, 25.0, 25.0, 25.0)
    with pytest.raises(ZeroDivisionError):
        mostrar_dados([linha])


# --------------------------------------------------------------------------
# funcmenu
# --------------------------------------------------------------------------

@pytest.mark.parametrize("entrada", ["1", "2", "5"])
def test_funcmenu_retorna_opcao_digitada(monkeypatch, entrada):
    """funcmenu devolve, como inteiro, a opção digitada pelo usuário."""
    monkeypatch.setattr("builtins.input", lambda _prompt="": entrada)
    assert funcmenu() == int(entrada)


def test_funcmenu_rejeita_entrada_nao_numerica(monkeypatch):
    """Entrada não numérica quebra o ``int(input(...))`` sem tratamento."""
    monkeypatch.setattr("builtins.input", lambda _prompt="": "abc")
    with pytest.raises(ValueError):
        funcmenu()
