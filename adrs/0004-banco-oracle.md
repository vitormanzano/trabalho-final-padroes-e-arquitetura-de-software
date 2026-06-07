# ADR-004: Adotar banco de dados relacional Oracle

- **Status:** Superseded by [ADR-005](0005-migrar-para-postgresql.md)
- **Data:** 2026-05-20
- **Decisores:** equipe do projeto

## Contexto

Os dados de produto são estruturados e tabulares (código, nome, descrição, custos,
impostos, comissão, margem e preço) e exigem integridade e consultas simples. A
disciplina de banco de dados do semestre adotou **Oracle** como SGBD de referência,
e a equipe seguiu essa orientação para alinhar o projeto ao conteúdo ensinado. A
conexão foi feita com a edição gratuita Oracle XE.

## Decisão

Persistir os dados em um banco **Oracle (XE)**, com os produtos armazenados em uma
tabela única.

## Consequências

### Benefícios
- Integridade referencial e consultas declarativas.
- Alinhamento direto ao conteúdo da disciplina de banco de dados.

### Custos
- Superdimensionamento para um cadastro de uma única tabela.
- Instalação e configuração trabalhosas.
- Dependência de um servidor dedicado para operar.

> Esta decisão foi **substituída pelo [ADR-005](0005-migrar-para-postgresql.md)**,
> por ser desproporcional ao porte do sistema.
