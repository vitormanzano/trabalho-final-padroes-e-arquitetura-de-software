"""Estratégias de precificação (padrão Strategy).

"""

from abc import ABC, abstractmethod

from src.domain.produto import Produto


class StrategyPreco(ABC):
    """Strategy: contrato de cálculo de preço de venda."""

    @abstractmethod
    def calcular(self, produto: Produto) -> float:
        ...


class PrecoPorMarkup(StrategyPreco):
    """Markup sobre o custo, descontando os percentuais (fórmula padrão).

    PV = 100 * custo / (100 - (custo_fixo + comissão + imposto + margem))
    """

    def calcular(self, produto: Produto) -> float:
        denominador = 100 - (
            produto.custo_fixo + produto.comissao
            + produto.imposto + produto.margem_lucro
        )
        if denominador <= 0:
            raise ValueError(
                "A soma dos percentuais (custo fixo + comissão + imposto + margem) "
                "deve ser menor que 100."
            )
        return 100 * produto.custo_produto / denominador


class PrecoMargemSobreCusto(StrategyPreco):
    """Precificação simples: aplica a margem diretamente sobre o custo.

    PV = custo * (1 + margem / 100)
    """

    def calcular(self, produto: Produto) -> float:
        return produto.custo_produto * (1 + produto.margem_lucro / 100)
