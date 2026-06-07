# Architecture Decision Records (ADRs)

Este diretório reúne as decisões arquiteturais relevantes do projeto **Cadastro de
Produtos para Sistema de Estoque**, registradas no formato canônico de ADR
(*Architecture Decision Record*), proposto por Michael Nygard. Cada decisão é um
arquivo próprio, com Número e título, Status, Contexto, Decisão e Consequências.

Os ADRs são imutáveis: quando uma decisão muda, um novo ADR é criado e o anterior
passa a `Superseded by ADR-XXX`, preservando o histórico do raciocínio.

| ADR | Título | Status |
| --- | --- | --- |
| [ADR-001](0001-adotar-python.md) | Adotar Python como linguagem principal | Accepted |
| [ADR-002](0002-monolito-procedural.md) | Adotar estrutura monolítica procedural, sem camadas | Superseded by ADR-003 |
| [ADR-003](0003-arquitetura-em-camadas.md) | Adotar arquitetura de monolito modular em camadas | Accepted |
| [ADR-004](0004-banco-oracle.md) | Adotar banco de dados relacional Oracle | Superseded by ADR-005 |
| [ADR-005](0005-migrar-para-postgresql.md) | Migrar o banco de dados Oracle para PostgreSQL | Accepted |
| [ADR-006](0006-interface-cli.md) | Adotar interface de linha de comando (CLI) | Accepted |
| [ADR-007](0007-repository-com-interface.md) | Encapsular o acesso a dados com o padrão Repository | Accepted |
| [ADR-008](0008-singleton-conexao.md) | Centralizar a conexão com o banco usando Singleton | Accepted |
| [ADR-009](0009-factory-method.md) | Compor as dependências com Factory Method | Accepted |
| [ADR-010](0010-strategy-precificacao.md) | Tornar a precificação intercambiável com Strategy | Accepted |

## Decisões revertidas ou modificadas

- **ADR-002 → ADR-003**: a estrutura procedural inicial foi substituída pela
  arquitetura em camadas.
- **ADR-004 → ADR-005**: o banco Oracle foi substituído pelo PostgreSQL, por ser
  desproporcional ao porte do sistema.
