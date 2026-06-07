# ADR-001: Adotar Python como linguagem principal

- **Status:** Accepted
- **Data:** 2026-05-19
- **Decisores:** equipe do projeto

## Contexto

A equipe precisava escolher uma linguagem para implementar um sistema de cadastro
de pequeno porte, no contexto de um curso de Engenharia de Software, com prazo
limitado e integrantes em diferentes níveis de experiência. As disciplinas do
semestre já forneciam base em Python, e o requisito de não escopo previa o uso de
uma única linguagem de programação.

## Decisão

Adotar **Python** como linguagem única do projeto, tanto no código legado quanto
na refatoração.

## Consequências

### Benefícios
- Curva de aprendizado baixa e código legível para toda a equipe.
- Vasto ecossistema de bibliotecas (incluindo `psycopg2` e `pytest`).
- Aderência direta ao conteúdo das disciplinas do semestre.

### Custos
- Desempenho inferior ao de linguagens compiladas — irrelevante para o volume de
  dados deste sistema.
- Tipagem dinâmica exige cuidados extras, mitigados por validação explícita
  (`validar_produto`) e anotações de tipo.
