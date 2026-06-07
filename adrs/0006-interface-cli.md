# ADR-006: Adotar interface de linha de comando (CLI)

- **Status:** Accepted
- **Data:** 2026-05-20
- **Decisores:** equipe do projeto

## Contexto

Era preciso definir a forma de interação com o usuário. Uma interface gráfica ou web
aumentaria a complexidade e o esforço sem agregar valor essencial ao domínio, que é
orientado a operações de cadastro (criar, listar, alterar, excluir).

## Decisão

Implementar a interação por meio de uma **interface de linha de comando** (`src/presentation/cli.py`),
com menu numérico e fluxos conduzidos campo a campo no terminal. A CLI depende
apenas do `ProdutoService`, sem conhecer SQL nem regras de negócio.

## Consequências

### Benefícios
- Simplicidade de implementação e foco no domínio.
- Operação previsível, apoiando o atributo de capacidade de interação.
- Camada de apresentação fina e desacoplada do restante.

### Custos
- Experiência visual limitada e menor apelo estético.
- Aceitável para o escopo acadêmico e o público interno previsto.
