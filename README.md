# Cadastro de Produtos para Sistema de Estoque

Sistema de linha de comando (CLI) em Python para cadastro, consulta, alteração e exclusão de produtos, com cálculo automático de preço de venda.

Trabalho final da disciplina de Padrões e Arquitetura de Software.

## Pré-requisitos

- Python 3.11 ou superior
- Docker e Docker Compose

## Instalação

1. Clone o repositório e entre na pasta:

```bash
git clone <url-do-repositorio>
cd trabalho-final-padroes-e-arquitetura-de-software
```

2. Instale as dependências Python:

```bash
pip install psycopg2-binary pytest pytest-cov
```

3. Crie o arquivo `.env` a partir do exemplo e preencha as credenciais:

```bash
cp .env.example .env
```

O `.env` deve conter:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=produtos
DB_USER=postgres
DB_PASSWORD=postgres
```

## Execução

1. Suba o banco de dados PostgreSQL via Docker:

```bash
docker compose up -d
```

2. Execute a aplicação:

```bash
python main.py
```

O sistema criará a tabela automaticamente na primeira execução.

## Testes

```bash
python -m pytest -v
```

Com relatório de cobertura:

```bash
python -m pytest --cov=src --cov-report=term-missing
```

## Estrutura do projeto

```
src/
  domain/        # Entidades e regras de negócio (Produto, validacao, cifra, strategy_preco)
  service/       # Camada de serviço — orquestração das regras
  repository/    # Contrato (IProdutoRepository) e implementação PostgreSQL
  presentation/  # Interface CLI e formatador
  factory/       # Factory Method para composição de repositório e serviço
  data/          # Conexão Singleton e esquema do banco
adrs/            # Architecture Decision Records (ADR-001 a ADR-010)
diagramas/       # Diagramas Mermaid (.mmd) e imagens (.png)
pi_legado/       # Código legado do Projeto Integrador (ponto de partida da refatoração)
tests/           # Testes automatizados (legado e refatorado)
```
