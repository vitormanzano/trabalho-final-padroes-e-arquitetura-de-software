# ADR-008: Centralizar a conexão com o banco usando Singleton

- **Status:** Accepted
- **Data:** 2026-05-27
- **Decisores:** equipe do projeto

## Contexto

Cada operação de cadastro, listagem ou exclusão poderia abrir uma nova conexão com o
PostgreSQL, desperdiçando recursos e dificultando o controle do ciclo de vida
(abrir/fechar) da conexão.

## Decisão

Aplicar o padrão **Singleton** na classe `DatabaseConnection` (`src/data/connection.py`),
garantindo uma única instância e uma única conexão compartilhada por toda a
aplicação, criada sob demanda (lazy). O acesso é feito pela função `conectar_banco()`.

## Consequências

### Benefícios
- Controle centralizado de um recurso caro (a conexão), evitando desperdício.
- Ponto único para abrir e fechar a conexão.

### Custos
- Introduz estado global, o que dificulta certos testes e oculta a dependência.
- A implementação **não é thread-safe**: sob concorrência, duas threads poderiam
  criar instâncias simultâneas. Aceitável para uma CLI sequencial; exigiria um
  *lock* caso a concorrência se torne requisito.
