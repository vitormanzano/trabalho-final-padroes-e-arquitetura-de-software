# ADR-009: Compor as dependências com Factory Method

- **Status:** Accepted
- **Data:** 2026-06-06
- **Decisores:** equipe do projeto

## Contexto

A construção direta do repositório e do serviço (`ProdutoRepository(conectar_banco())`)
no ponto de composição amarrava o cliente à implementação concreta de persistência.
Era desejável poder trocar a fonte de dados (PostgreSQL, mock, outro SGBD) sem
alterar quem consome o repositório/serviço.

## Decisão

Aplicar o padrão **Factory Method** com criadores abstratos e concretos:
`RepositoryCreator` / `PostgresRepositoryCreator` (produz `IProdutoRepository`) e
`ServiceCreator` / `PostgresServiceCreator` (produz `ProdutoService` já composto). O
`main` passou a obter o serviço por meio do criador, sem instanciar o repositório
diretamente.

## Consequências

### Benefícios
- Desacoplamento do cliente em relação às implementações concretas.
- Extensão por subclasse: uma nova fonte de dados é um novo criador, sem tocar no
  `main` nem na CLI.
- Combina com o Repository ([ADR-007](0007-repository-com-interface.md)).

### Custos
- Com uma única implementação concreta por criador, o padrão agrega sobretudo valor
  demonstrativo; o ganho efetivo aparece a partir da segunda implementação.

> **Nota de evolução:** uma versão inicial colocava a montagem do serviço dentro do
> criador de repositório (`criar_servico`), o que tornava o nome da classe
> incoerente com o que ela produzia. A decisão foi **ajustada**, separando os papéis
> em `RepositoryCreator` (cria repositório) e `ServiceCreator` (cria serviço).
