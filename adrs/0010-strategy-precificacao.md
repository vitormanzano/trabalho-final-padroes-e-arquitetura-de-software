# ADR-010: Tornar a precificação intercambiável com Strategy

- **Status:** Accepted
- **Data:** 2026-06-06
- **Decisores:** equipe do projeto

## Contexto

A fórmula de cálculo do preço de venda estava fixa dentro da entidade `Produto`.
Previa-se que a regra de precificação pudesse variar (markup, margem sobre custo e,
futuramente, descontos ou políticas por contexto), e não era desejável alterar a
camada de serviço a cada nova regra.

## Decisão

Aplicar o padrão **Strategy**: extrair o cálculo para o contrato `StrategyPreco`
(`src/domain/strategy_preco.py`), com as implementações `PrecoPorMarkup` (padrão) e
`PrecoMargemSobreCusto`. O `ProdutoService` atua como contexto, recebendo a estratégia
por injeção e expondo `calcular_preco`. A escolha da estratégia é feita na
`ServiceFactory`.

## Consequências

### Benefícios
- Abertura para extensão sem modificação (OCP): uma nova política de preço é uma
  nova classe, sem alterar o serviço.
- Cada algoritmo é testado isoladamente; o contexto é testado com uma estratégia
  conhecida.

### Custos
- Aumento no número de classes e uma indireção a mais.
- Para poucas variações, uma função simples bastaria; o ganho compensa quando as
  regras de precificação tendem a crescer.

> **Nota de nomenclatura:** a classe foi padronizada como `StrategyPreco` (arquivo
> `strategy_preco.py`), após um período de divergência com o nome `EstrategiaPreco`,
> que chegou a quebrar a importação até ser consolidado.
