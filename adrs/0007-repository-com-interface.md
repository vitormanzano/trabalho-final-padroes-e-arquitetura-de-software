# ADR-007: Encapsular o acesso a dados com o padrão Repository

- **Status:** Accepted
- **Data:** 2026-05-27
- **Decisores:** equipe do projeto

## Contexto

Com a arquitetura em camadas ([ADR-003](0003-arquitetura-em-camadas.md)), era preciso
impedir que as regras de negócio dependessem diretamente do SQL e da API do banco.
No código legado, o acesso a dados estava entrelaçado com a lógica, o que dificultava
testes e a futura troca de SGBD — troca que de fato ocorreu
([ADR-005](0005-migrar-para-postgresql.md)).

## Decisão

Encapsular o acesso a dados com o padrão **Repository**, definindo o contrato de
domínio `IProdutoRepository` (interface) e a implementação concreta
`ProdutoRepository` (SQL PostgreSQL). O `ProdutoService` depende da **interface**, não
da implementação. A criptografia e a validação ficam no serviço; o repositório
trata apenas de SQL.

## Consequências

### Benefícios
- Desacoplamento entre regra de negócio e tecnologia de persistência — comprovado na
  migração Oracle → PostgreSQL.
- Testabilidade: o serviço é testado com um repositório falso (mock), sem banco real.
- Centralização do acesso a dados em um único ponto.

### Custos
- Mais código e indireção para uma única entidade.
- A abstração ainda vaza parcialmente: a assinatura expõe o tipo
  `psycopg2.extensions.connection` (ver dívida técnica em análise futura).
