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
