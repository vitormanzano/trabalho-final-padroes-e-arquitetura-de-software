"""Testes do código refatorado.

Espelha os testes de caracterização do legado (tests/teste_legado/test_funcoes.py),
garantindo que o comportamento observável seja preservado após a refatoração.

Cobertura:
- ``cifra.criptografar``        — cifra de substituição usada no cadastro.
- ``cifra.descriptografar``     — operação inversa, usada na listagem.
- ``domain.Produto``            — classificação de rentabilidade.
- ``domain.strategy_preco``     — Strategy: estratégias de precificação.
- ``domain.validacao``          — regras de validação de produto.
- ``service.ProdutoService``    — cadastro, listagem, alteração, exclusão e cifra.
- ``repository``                — contrato ``IProdutoRepository`` e implementação.
- ``factory``                   — Factory Method de repository e de service.
- ``presentation.formatador``   — formatação de produto para exibição.

Como rodar:
    python -m pytest -v
    python -m pytest --cov=src --cov-report=term-missing
"""

from unittest.mock import MagicMock, patch

import pytest

from src.domain.cifra import criptografar, descriptografar
from src.domain.strategy_preco import PrecoMargemSobreCusto, PrecoPorMarkup
from src.domain.produto import Produto
from src.domain.validacao import ErroValidacao, validar_produto
from src.factory.repository_factory import PostgresRepositoryCreator, RepositoryCreator
from src.factory.service_factory import PostgresServiceCreator, ServiceCreator
from src.presentation.formatador import formatar_produto
from src.repository.produto_repository import IProdutoRepository, ProdutoRepository
from src.service.produto_service import ProdutoService


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
# Strategy — estratégias de precificação
# ---------------------------------------------------------------------------

def test_preco_por_markup_resultado_correto():
    """PrecoPorMarkup: PV = 100 * custo / (100 - soma_percentuais)."""
    produto = _produto(margem_lucro=25.0)
    # 100 - (10 + 5 + 8 + 25) = 52  →  PV = 100 * 100 / 52 ≈ 192.31
    esperado = 100 * 100.0 / (100 - (10.0 + 5.0 + 8.0 + 25.0))
    assert PrecoPorMarkup().calcular(produto) == pytest.approx(esperado, rel=1e-4)


def test_preco_por_markup_soma_cem_lanca_erro():
    """Soma dos percentuais igual a 100 deve lançar ValueError."""
    produto = Produto(1, "X", "Y", 100.0, 25.0, 25.0, 25.0, 25.0)
    with pytest.raises(ValueError):
        PrecoPorMarkup().calcular(produto)


def test_preco_por_markup_soma_acima_de_cem_lanca_erro():
    """Soma dos percentuais acima de 100 deve lançar ValueError."""
    produto = Produto(1, "X", "Y", 100.0, 30.0, 30.0, 30.0, 30.0)
    with pytest.raises(ValueError):
        PrecoPorMarkup().calcular(produto)


def test_preco_margem_sobre_custo_resultado_correto():
    """PrecoMargemSobreCusto: PV = custo * (1 + margem / 100)."""
    produto = _produto(margem_lucro=25.0)
    assert PrecoMargemSobreCusto().calcular(produto) == pytest.approx(125.0)


def test_estrategias_de_preco_sao_intercambiaveis():
    """As duas estratégias produzem preços distintos para o mesmo produto."""
    produto = _produto(margem_lucro=25.0)
    assert PrecoPorMarkup().calcular(produto) != PrecoMargemSobreCusto().calcular(produto)


def test_service_usa_a_estrategia_injetada():
    """O service (contexto) delega o cálculo à estratégia recebida."""
    repo = MagicMock(spec=IProdutoRepository)
    produto = _produto(margem_lucro=25.0)

    servico_markup = ProdutoService(repo, PrecoPorMarkup())
    servico_custo  = ProdutoService(repo, PrecoMargemSobreCusto())

    assert servico_markup.calcular_preco(produto) == PrecoPorMarkup().calcular(produto)
    assert servico_custo.calcular_preco(produto) == PrecoMargemSobreCusto().calcular(produto)


def test_service_usa_markup_como_estrategia_padrao():
    """Sem estratégia explícita, o service usa PrecoPorMarkup."""
    repo = MagicMock(spec=IProdutoRepository)
    produto = _produto(margem_lucro=25.0)
    servico = ProdutoService(repo)
    assert servico.calcular_preco(produto) == PrecoPorMarkup().calcular(produto)


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
    repositorio = MagicMock(spec=ProdutoRepository)
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
    produto = _produto()
    saida = formatar_produto(produto, PrecoPorMarkup().calcular(produto))
    assert "Arroz" in saida
    assert "FEIJAO" in saida


def test_formatar_produto_contem_preco_de_venda():
    """A saída formatada deve conter a linha de preço de venda."""
    produto = _produto()
    saida = formatar_produto(produto, PrecoPorMarkup().calcular(produto))
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
    produto = _produto(margem_lucro=margem)
    saida = formatar_produto(produto, PrecoPorMarkup().calcular(produto))
    assert rotulo in saida


# ---------------------------------------------------------------------------
# ProdutoService — cifra (a criptografia migrou do repository para o service)
# ---------------------------------------------------------------------------

def test_cadastrar_produto_cifra_descricao_antes_de_salvar():
    """O service deve persistir a descrição já cifrada."""
    servico, repo = _servico_com_mock()
    repo.buscar_por_id.return_value = None

    servico.cadastrar_produto(1, "Arroz", "GRAO", 100.0, 10.0, 5.0, 8.0, 25.0)

    produto_salvo = repo.salvar.call_args.args[0]
    assert produto_salvo.descricao == criptografar("GRAO")


def test_cadastrar_produto_retorna_descricao_em_texto_claro():
    """O produto devolvido ao chamador mantém a descrição legível."""
    servico, repo = _servico_com_mock()
    repo.buscar_por_id.return_value = None

    produto = servico.cadastrar_produto(1, "Arroz", "GRAO", 100.0, 10.0, 5.0, 8.0, 25.0)

    assert produto.descricao == "GRAO"


def test_buscar_produto_decifra_descricao():
    """buscar_produto deve devolver a descrição decifrada."""
    servico, repo = _servico_com_mock()
    repo.buscar_por_id.return_value = _produto(descricao=criptografar("GRAO"))

    produto = servico.buscar_produto(1)

    assert produto.descricao == "GRAO"


def test_listar_produtos_decifra_descricao():
    """listar_produtos deve devolver as descrições decifradas."""
    servico, repo = _servico_com_mock()
    repo.listar_todos.return_value = [_produto(descricao=criptografar("FEIJAO"))]

    produtos = servico.listar_produtos()

    assert produtos[0].descricao == "FEIJAO"


def test_atualizar_produto_cifra_descricao():
    """atualizar_produto deve persistir a descrição já cifrada."""
    servico, repo = _servico_com_mock()

    servico.atualizar_produto(_produto(descricao="GRAO"))

    produto_atualizado = repo.atualizar.call_args.args[0]
    assert produto_atualizado.descricao == criptografar("GRAO")


# ---------------------------------------------------------------------------
# Repository — contrato (interface de domínio)
# ---------------------------------------------------------------------------

def test_produto_repositorio_implementa_a_interface():
    assert issubclass(ProdutoRepository, IProdutoRepository)


def test_interface_repositorio_nao_e_instanciavel():
    with pytest.raises(TypeError):
        IProdutoRepository()


# ---------------------------------------------------------------------------
# Factory Method — repository e service
# ---------------------------------------------------------------------------

def test_creators_abstratos_nao_sao_instanciaveis():
    with pytest.raises(TypeError):
        RepositoryCreator()
    with pytest.raises(TypeError):
        ServiceCreator()


@patch("src.factory.repository_factory.conectar_banco")
def test_postgres_repository_creator_fabrica_repositorio(mock_conectar):
    """O método fábrica devolve um produto concreto do tipo esperado."""
    mock_conectar.return_value = MagicMock()

    repositorio = PostgresRepositoryCreator().criar_repository()

    assert isinstance(repositorio, ProdutoRepository)
    assert isinstance(repositorio, IProdutoRepository)


@patch("src.factory.repository_factory.conectar_banco")
def test_postgres_service_creator_fabrica_service(mock_conectar):
    """O service factory compõe um ProdutoService com seu repositório."""
    mock_conectar.return_value = MagicMock()

    servico = PostgresServiceCreator().criar_service()

    assert isinstance(servico, ProdutoService)


def test_service_creator_extensivel_sem_alterar_o_cliente():
    """Uma nova subclasse troca a fonte de dados — a essência do Factory Method."""
    repo_falso = MagicMock(spec=IProdutoRepository)
    repo_falso.listar_todos.return_value = []

    class FakeServiceCreator(ServiceCreator):
        def criar_service(self) -> ProdutoService:
            return ProdutoService(repo_falso)

    servico = FakeServiceCreator().criar_service()

    assert servico.listar_produtos() == []
    repo_falso.listar_todos.assert_called_once()
