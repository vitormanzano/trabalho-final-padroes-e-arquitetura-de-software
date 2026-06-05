"""Entidade de domínio: Produto.

Representa um produto do estoque com seus atributos financeiros.
Não depende de banco de dados nem de terminal.
"""

from dataclasses import dataclass


@dataclass
class Produto:
    id_produto: int
    nome: str
    descricao: str
    custo_produto: float
    custo_fixo: float
    comissao: float
    imposto: float
    margem_lucro: float

    def calcular_preco_venda(self) -> float:
        """Calcula o preço de venda a partir dos percentuais informados.

        Centraliza a fórmula em um único lugar, eliminando a duplicação
        que existia entre o cadastro e a listagem no código legado.
        """
        denominador = 100 - (
            self.custo_fixo + self.comissao + self.imposto + self.margem_lucro
        )
        if denominador <= 0:
            raise ValueError(
                "A soma dos percentuais (custo fixo + comissão + imposto + margem) "
                "deve ser menor que 100."
            )
        return 100 * self.custo_produto / denominador

    def classificar_rentabilidade(self) -> str:
        """Retorna o rótulo de rentabilidade com base na margem de lucro."""
        if self.margem_lucro > 20:
            return "Margem de lucro alta"
        if self.margem_lucro > 10:
            return "Margem de lucro média"
        if self.margem_lucro > 0:
            return "Margem de lucro baixa"
        if self.margem_lucro == 0:
            return "Equilíbrio"
        return "Prejuízo"
