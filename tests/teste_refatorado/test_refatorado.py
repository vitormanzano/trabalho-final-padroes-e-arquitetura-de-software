"""Testes do código refatorado.

Espelha os testes de caracterização do legado (tests/teste_legado/test_funcoes.py),
garantindo que o comportamento observável seja preservado após a refatoração.

Cobertura:
- ``cifra.criptografar``        — cifra de substituição usada no cadastro.
- ``cifra.descriptografar``     — operação inversa, usada na listagem.
- ``domain.Produto``            — cálculo de preço e classificação de rentabilidade.
- ``domain.validacao``          — regras de validação de produto.
- ``service.ProdutoService``    — cadastro, listagem, alteração e exclusão.
- ``presentation.formatador``   — formatação de produto para exibição.

Como rodar:
    python -m pytest -v
    python -m pytest --cov=src --cov-report=term-missing
"""

from unittest.mock import MagicMock

import pytest

from src.domain.cifra import criptografar, descriptografar
from src.domain.produto import Produto
from src.domain.validacao import ErroValidacao, validar_produto
from src.presentation.formatador import formatar_produto
from src.service.produto_service import ProdutoRepositorio, ProdutoService


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _produto(margem_lucro: float = 25.0, descricao: str = "FEIJAO") -> Produto:
    """Cria um produto padrão para uso nos testes."""
    return Produto(
        id_produto=1,
        nome="Arroz",
        descricao=descricao,
        custo_produto=100.0,
        custo_fixo=10.0,
        comissao=5.0,
        imposto=8.0,
        margem_lucro=margem_lucro,
    )


# ---------------------------------------------------------------------------
# criptografar
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("texto, esperado", [
    ("OI", "IG"),
    ("BANANA", "KDGPGP"),
    ("CASA", "OEAU"),
])
def test_criptografar_valores_conhecidos(texto, esperado):
    """Valores de referência (golden values) extraídos do comportamento legado."""
    assert criptografar(texto) == esperado


def test_criptografar_ignora_caixa():
    """O texto é convertido para maiúsculas antes de cifrar."""
    assert criptografar("casa") == criptografar("CASA")


def test_criptografar_remove_espacos():
    """Espaços são descartados antes de cifrar."""
    assert criptografar("A B C D") == criptografar("ABCD")


def test_criptografar_texto_impar_duplica_ultima_letra():
    """Texto de comprimento ímpar recebe padding: a última letra é repetida."""
    assert criptografar("A") == criptografar("AA")


def test_criptografar_string_vazia_retorna_vazia():
    assert criptografar("") == ""


def test_criptografar_rejeita_caractere_fora_do_alfabeto():
    """Dígitos e acentos não estão na tabela A–Z e devem lançar ValueError."""
    with pytest.raises(ValueError):
        criptografar("TESTE1")


# ---------------------------------------------------------------------------
# descriptografar
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("texto", ["OI", "BANANA", "CASA", "FEIJAO"])
def test_roundtrip_texto_par(texto):
    """Texto de comprimento par volta ao original após cifrar e decifrar."""
    assert descriptografar(criptografar(texto)) == texto


def test_roundtrip_texto_impar_mantem_padding():
    """Texto ímpar não volta idêntico — o padding duplica a última letra."""
    assert descriptografar(criptografar("TESTE")) == "TESTEE"


# ---------------------------------------------------------------------------
# Produto — calcular_preco_venda
# ---------------------------------------------------------------------------

def test_calcular_preco_venda_resultado_correto():
    """Verifica a fórmula: PV = 100 * custo / (100 - soma_percentuais)."""
    produto = _produto(margem_lucro=25.0)
    # 100 - (10 + 5 + 8 + 25) = 52  →  PV = 100 * 100 / 52 ≈ 192.31
    esperado = 100 * 100.0 / (100 - (10.0 + 5.0 + 8.0 + 25.0))
    assert produto.calcular_preco_venda() == pytest.approx(esperado, rel=1e-4)


def test_calcular_preco_venda_soma_cem_lanca_erro():
    """Soma dos percentuais igual a 100 deve lançar ValueError."""
    produto = Produto(1, "X", "Y", 100.0, 25.0, 25.0, 25.0, 25.0)
    with pytest.raises(ValueError):
        produto.calcular_preco_venda()


def test_calcular_preco_venda_soma_acima_de_cem_lanca_erro():
    """Soma dos percentuais acima de 100 deve lançar ValueError."""
    produto = Produto(1, "X", "Y", 100.0, 30.0, 30.0, 30.0, 30.0)
    with pytest.raises(ValueError):
        produto.calcular_preco_venda()


# ---------------------------------------------------------------------------
# Produto — classificar_rentabilidade
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("margem, rotulo", [
    (25.0,  "Margem de lucro alta"),
    (15.0,  "Margem de lucro média"),
    (5.0,   "Margem de lucro baixa"),
    (0.0,   "Equilíbrio"),
    (-5.0,  "Prejuízo"),
])
def test_classificar_rentabilidade(margem, rotulo):
    """Cada faixa de margem de lucro gera o rótulo correto."""
    assert _produto(margem_lucro=margem).classificar_rentabilidade() == rotulo


# ---------------------------------------------------------------------------
# validar_produto
# ---------------------------------------------------------------------------

def test_validar_produto_dados_validos_nao_lanca():
    """Dados válidos não devem lançar nenhuma exceção."""
    validar_produto(1, "Arroz", "Grão", 100.0, 10.0, 5.0, 8.0, 25.0)


def test_validar_produto_id_zero_lanca_erro():
    with pytest.raises(ErroValidacao) as info:
        validar_produto(0, "Arroz", "Grão", 100.0, 10.0, 5.0, 8.0, 25.0)
    assert info.value.campo == "id_produto"


def test_validar_produto_nome_vazio_lanca_erro():
    with pytest.raises(ErroValidacao) as info:
        validar_produto(1, "", "Grão", 100.0, 10.0, 5.0, 8.0, 25.0)
    assert info.value.campo == "nome"


def test_validar_produto_descricao_vazia_lanca_erro():
    with pytest.raises(ErroValidacao) as info:
        validar_produto(1, "Arroz", "", 100.0, 10.0, 5.0, 8.0, 25.0)
    assert info.value.campo == "descricao"


def test_validar_produto_custo_negativo_lanca_erro():
    with pytest.raises(ErroValidacao) as info:
        validar_produto(1, "Arroz", "Grão", -1.0, 10.0, 5.0, 8.0, 25.0)
    assert info.value.campo == "custo_produto"


def test_validar_produto_soma_percentuais_cem_lanca_erro():
    with pytest.raises(ErroValidacao) as info:
        validar_produto(1, "Arroz", "Grão", 100.0, 25.0, 25.0, 25.0, 25.0)
    assert info.value.campo == "margem_lucro"


# ---------------------------------------------------------------------------
# ProdutoService — usando repositório falso (mock)
# ---------------------------------------------------------------------------

def _servico_com_mock():
    """Cria um ProdutoService com repositório mockado."""
    repositorio = MagicMock(spec=ProdutoRepositorio)
    return ProdutoService(repositorio), repositorio


def test_cadastrar_produto_chama_salvar():
    """cadastrar_produto deve chamar repositorio.salvar uma vez."""
    servico, repo = _servico_com_mock()
    repo.buscar_por_id.return_value = None

    servico.cadastrar_produto(1, "Arroz", "GRAO", 100.0, 10.0, 5.0, 8.0, 25.0)

    repo.salvar.assert_called_once()


def test_cadastrar_produto_id_duplicado_lanca_erro():
    """cadastrar_produto deve lançar ValueError se o id já existir."""
    servico, repo = _servico_com_mock()
    repo.buscar_por_id.return_value = _produto()

    with pytest.raises(ValueError):
        servico.cadastrar_produto(1, "Arroz", "GRAO", 100.0, 10.0, 5.0, 8.0, 25.0)


def test_cadastrar_produto_dados_invalidos_nao_chama_salvar():
    """cadastrar_produto não deve persistir se a validação falhar."""
    servico, repo = _servico_com_mock()
    repo.buscar_por_id.return_value = None

    with pytest.raises(ErroValidacao):
        servico.cadastrar_produto(0, "Arroz", "GRAO", 100.0, 10.0, 5.0, 8.0, 25.0)

    repo.salvar.assert_not_called()


def test_listar_produtos_retorna_lista_do_repositorio():
    servico, repo = _servico_com_mock()
    repo.listar_todos.return_value = [_produto()]

    resultado = servico.listar_produtos()

    assert len(resultado) == 1
    assert resultado[0].nome == "Arroz"


def test_excluir_produto_id_inexistente_lanca_erro():
    servico, repo = _servico_com_mock()
    repo.buscar_por_id.return_value = None

    with pytest.raises(ValueError):
        servico.excluir_produto(99)

    repo.excluir.assert_not_called()


def test_excluir_produto_chama_excluir_no_repositorio():
    servico, repo = _servico_com_mock()
    repo.buscar_por_id.return_value = _produto()

    servico.excluir_produto(1)

    repo.excluir.assert_called_once_with(1)


def test_atualizar_produto_dados_invalidos_nao_chama_atualizar():
    servico, repo = _servico_com_mock()
    produto_invalido = Produto(0, "", "GRAO", 100.0, 10.0, 5.0, 8.0, 25.0)

    with pytest.raises(ErroValidacao):
        servico.atualizar_produto(produto_invalido)

    repo.atualizar.assert_not_called()


# ---------------------------------------------------------------------------
# formatador
# ---------------------------------------------------------------------------

def test_formatar_produto_contem_nome_e_descricao():
    """A saída formatada deve conter o nome e a descrição do produto."""
    saida = formatar_produto(_produto())
    assert "Arroz" in saida
    assert "FEIJAO" in saida


def test_formatar_produto_contem_preco_de_venda():
    """A saída formatada deve conter a linha de preço de venda."""
    saida = formatar_produto(_produto())
    assert "Preço de venda" in saida


@pytest.mark.parametrize("margem, rotulo", [
    (25.0,  "Margem de lucro alta"),
    (15.0,  "Margem de lucro média"),
    (5.0,   "Margem de lucro baixa"),
    (0.0,   "Equilíbrio"),
    (-5.0,  "Prejuízo"),
])
def test_formatar_produto_classifica_rentabilidade(margem, rotulo):
    """Cada faixa de margem deve aparecer no texto formatado."""
    saida = formatar_produto(_produto(margem_lucro=margem))
    assert rotulo in saida
