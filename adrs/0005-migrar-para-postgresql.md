# ADR-005: Migrar o banco de dados Oracle para PostgreSQL

- **Status:** Accepted
- **Data:** 2026-06-04
- **Decisores:** equipe do projeto
- **Supersedes:** [ADR-004](0004-banco-oracle.md)

## Contexto

A escolha do Oracle ([ADR-004](0004-banco-oracle.md)) mostrou-se desproporcional ao
porte do sistema: um cadastro com uma única tabela, um único usuário e execução
local não justifica um SGBD corporativo. Os custos mais relevantes foram a
instalação e configuração trabalhosas e a dependência de um servidor dedicado. Esta
foi uma **decisão revertida** durante o desenvolvimento.

## Decisão

Migrar a persistência para o **PostgreSQL**, mantendo o modelo de dados em uma única
tabela de produtos. A migração envolveu substituir o driver Oracle pelo driver
`psycopg2`, ajustar os parâmetros de conexão (lidos do `.env`) e adaptar os tipos de
coluna do esquema e as consultas para a sintaxe do PostgreSQL. Um `docker-compose`
passou a provisionar o banco para execução local.

## Consequências

### Benefícios
- Sem custos de licenciamento; proporcional ao porte do sistema.
- Provisionamento simples e reprodutível via contêiner.
- Independência de um servidor dedicado.

### Custos
- Esforço de migração (driver, esquema e consultas).
- Necessidade de manter um ambiente Docker para desenvolvimento.

> **Nota de implementação:** durante a migração houve uma tentativa transitória de
> usar o driver `psycopg` (v3); o projeto consolidou-se no `psycopg2`, efetivamente
> instalado e compatível com a camada de conexão.
