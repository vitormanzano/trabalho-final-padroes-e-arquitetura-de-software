"""Formatação de produtos para exibição no terminal.

Responsabilidade única: transformar um objeto Produto em texto formatado.
Não conhece banco de dados nem regras de negócio.
"""

from src.domain.produto import Produto


def formatar_produto(produto: Produto, preco_venda: float) -> str:
    """Retorna a representação textual completa de um produto.

    O preço de venda é calculado fora (pela estratégia de precificação do
    serviço) e injetado aqui, mantendo a formatação livre de regra de negócio.
    """
    pv = preco_venda

    receita_bruta  = pv - produto.custo_produto
    custo_fixo_rs  = pv * produto.custo_fixo / 100
    comissao_rs    = pv * produto.comissao / 100
    imposto_rs     = pv * produto.imposto / 100
    outros_custos  = custo_fixo_rs + comissao_rs + imposto_rs
    margem_reais   = produto.margem_lucro * pv / 100

    cp_pct      = 100 * produto.custo_produto / pv
    receita_pct = 100 * receita_bruta / pv
    outros_pct  = 100 * outros_custos / pv

    linhas = [
        f"\t\t{produto.id_produto} {produto.nome}\t\t{produto.descricao}",
        "",
        f"{'Descrição':<25} {'Valor':>12}  {'%':>8}",
        f"{'Preço de venda:':<25} R${pv:>9.2f}  {'100,00%':>8}",
        f"{'Preço de compra:':<25} R${produto.custo_produto:>9.2f}  {cp_pct:>7.2f}%",
        f"{'Receita bruta:':<25} R${receita_bruta:>9.2f}  {receita_pct:>7.2f}%",
        f"{'Custo fixo:':<25} R${custo_fixo_rs:>9.2f}  {produto.custo_fixo:>7.2f}%",
        f"{'Comissão de vendas:':<25} R${comissao_rs:>9.2f}  {produto.comissao:>7.2f}%",
        f"{'Impostos:':<25} R${imposto_rs:>9.2f}  {produto.imposto:>7.2f}%",
        f"{'Outros custos:':<25} R${outros_custos:>9.2f}  {outros_pct:>7.2f}%",
        f"{'Rentabilidade:':<25} R${margem_reais:>9.2f}  {produto.margem_lucro:>7.2f}%",
        f"Lucro: {produto.classificar_rentabilidade()}",
        "",
    ]
    return "\n".join(linhas)
