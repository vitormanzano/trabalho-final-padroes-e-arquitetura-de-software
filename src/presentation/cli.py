"""Interface de linha de comando (CLI).

Responsabilidade única: interagir com o usuário.
Não contém nenhuma regra de negócio nem acesso a banco.
"""

from src.domain.produto import Produto
from src.domain.validacao import ErroValidacao
from src.presentation.formatador import formatar_produto
from src.service.produto_service import ProdutoService

_BANNER = """\n
==========================================================================
|    BBBBB   EEEEE   M   M         V   V   IIIII   N   N   DDDD    OOOO  |
|    B    B  E       MM MM         V   V     I     NN  N   D   D  O    O |
|    BBBBB   EEEE    M M M          V V      I     N N N   D   D  O    O |
|    B    B  E       M   M          V V      I     N  NN   D   D  O    O |
|    BBBBB   EEEEE   M   M           V     IIIII   N   N   DDDD    OOOO  |
==========================================================================
      |              SISTEMA DE CADASTRO DE PRODUTOS                |
      |                  PARA SISTEMAS DE ESTOQUE                   |
      =============================================================="""

_MENU_PRINCIPAL = """
        --------------------------------------
        |     DIGITE A OPÇÃO QUE DESEJAR!    |
        --------------------------------------
    1- Cadastrar Produto   2- Ver Produtos Cadastrados

    3- Alterar Produto     4- Exclusão de Produto

                    5- Sair
"""

_MENU_ALTERAR = """
        ---------------------------------------------
        |     CAMPO QUE DESEJA ALTERAR              |
        ---------------------------------------------
    1- ID          2- Nome        3- Descrição
    4- Custo       5- Custo Fixo  6- Comissão
    7- Imposto     8- Margem de Lucro
"""

_CAMPOS_ALTERAR = {
    1: "id_produto",
    2: "nome",
    3: "descricao",
    4: "custo_produto",
    5: "custo_fixo",
    6: "comissao",
    7: "imposto",
    8: "margem_lucro",
}


class CLI:
    """Ponto de entrada da interface de linha de comando."""

    def __init__(self, servico: ProdutoService) -> None:
        self._servico = servico

    def iniciar(self) -> None:
        print(_BANNER)
        opcao = self._ler_menu()
        while opcao != 5:
            try:
                self._despachar(opcao)
            except (ErroValidacao, ValueError) as erro:
                print(f"\n\tErro: {erro}")
            except Exception as erro:
                print(f"\n\tErro inesperado: {erro}")
            opcao = self._ler_menu()
        print("\nPrograma encerrado.")

    def _despachar(self, opcao: int) -> None:
        acoes = {
            1: self._cadastrar,
            2: self._listar,
            3: self._alterar,
            4: self._excluir,
        }
        acao = acoes.get(opcao)
        if acao is None:
            print("\n\tDIGITE UM NÚMERO CORRESPONDENTE A UMA AÇÃO DO MENU")
        else:
            acao()

    def _cadastrar(self) -> None:
        print("\n\t\t<<< Cadastro de produto >>>\n")
        id_produto    = self._ler_int("ID do produto: ")
        nome          = input("Nome do produto: ").strip()
        descricao     = input("Descrição: ").strip()
        custo_produto = self._ler_float("Custo do produto: ")
        imposto       = self._ler_float("Imposto (%): ")
        comissao      = self._ler_float("Comissão da venda (%): ")
        custo_fixo    = self._ler_float("Custo fixo (%): ")
        margem_lucro  = self._ler_float("Rentabilidade (%): ")

        produto = self._servico.cadastrar_produto(
            id_produto, nome, descricao,
            custo_produto, custo_fixo, comissao, imposto, margem_lucro,
        )
        print(f"\nLucro: {produto.classificar_rentabilidade()}")
        print("\nDados inseridos com sucesso.")

    def _listar(self) -> None:
        print("\n\t\t<<< Lista de produtos >>>\n")
        produtos = self._servico.listar_produtos()
        if not produtos:
            print("\tNenhum produto cadastrado.")
            return
        for produto in produtos:
            print(formatar_produto(produto))

    def _alterar(self) -> None:
        print("\n\t\t<<< Alteração de cadastro >>>\n")
        id_produto = self._ler_int("ID do produto que deseja alterar: ")
        produto = self._servico.buscar_produto(id_produto)
        if produto is None:
            print("\n\t\tO ID não existe!")
            return

        print(formatar_produto(produto))
        print(_MENU_ALTERAR)
        campo_opcao = self._ler_int("Opção: ")
        nome_campo  = _CAMPOS_ALTERAR.get(campo_opcao)
        if nome_campo is None:
            print("\tOpção inválida.")
            return

        novo_valor       = self._ler_valor_campo(nome_campo)
        produto_alterado = self._aplicar_alteracao(produto, nome_campo, novo_valor)
        self._servico.atualizar_produto(produto_alterado)
        print("\tProduto alterado com sucesso!")

    def _excluir(self) -> None:
        print("\n\t\t<<< Exclusão de produto >>>\n")
        id_produto = self._ler_int("ID do produto que deseja excluir: ")
        produto    = self._servico.buscar_produto(id_produto)
        if produto is None:
            print("\tO ID não existe!")
            return

        print(formatar_produto(produto))
        confirmacao = input("\tDeseja realmente excluir? s[SIM] n[NÃO]: ").strip().lower()
        if confirmacao == "s":
            self._servico.excluir_produto(id_produto)
            print("\t\tProduto excluído com sucesso!")
        elif confirmacao == "n":
            print("\tProduto não excluído.")
        else:
            print("\tOpção inválida.")

    def _ler_menu(self) -> int:
        return self._ler_int(_MENU_PRINCIPAL)

    def _ler_int(self, prompt: str) -> int:
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("\tDigite um número inteiro válido.")

    def _ler_float(self, prompt: str) -> float:
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("\tDigite um número válido.")

    def _ler_valor_campo(self, nome_campo: str) -> int | float | str:
        if nome_campo == "id_produto":
            return self._ler_int("Novo ID: ")
        if nome_campo in ("custo_produto", "custo_fixo", "comissao", "imposto", "margem_lucro"):
            return self._ler_float("Novo valor: ")
        return input("Novo valor: ").strip()

    @staticmethod
    def _aplicar_alteracao(produto: Produto, campo: str, valor) -> Produto:
        """Retorna nova instância de Produto com o campo atualizado."""
        dados = {
            "id_produto":    produto.id_produto,
            "nome":          produto.nome,
            "descricao":     produto.descricao,
            "custo_produto": produto.custo_produto,
            "custo_fixo":    produto.custo_fixo,
            "comissao":      produto.comissao,
            "imposto":       produto.imposto,
            "margem_lucro":  produto.margem_lucro,
        }
        dados[campo] = valor
        return Produto(**dados)
