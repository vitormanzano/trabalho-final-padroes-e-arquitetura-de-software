# ADR-002: Adotar estrutura monolítica procedural, sem camadas

- **Status:** Superseded by [ADR-003](0003-arquitetura-em-camadas.md)
- **Data:** 2026-05-19
- **Decisores:** equipe do projeto

## Contexto

O sistema é um cadastro de produtos de pequeno porte, operado por um único tipo de
usuário e executado localmente. No primeiro projeto integrador, diante desse
cenário, a equipe escolheu a abordagem mais direta possível: escrever o fluxo do
programa de forma sequencial, sem abstrações, priorizando a entrega rápida.

## Decisão

Adotar uma estrutura **monolítica e procedural**, sem separação em camadas e sem
orientação a objetos. A lógica fica concentrada em um script principal (`main.py`),
apoiado por módulos auxiliares (`funcoes.py`, `conexao.py`), conforme o diretório
`pi_legado/`. Não há camadas de apresentação, serviço e persistência separadas, não
há classes e não há padrões de projeto.

## Consequências

### Benefícios
- Simplicidade imediata e baixa sobrecarga inicial.
- Fácil de acompanhar de forma linear, de cima para baixo.

### Custos
- Baixa manutenibilidade e duplicação de lógica (ex.: cálculo de preço repetido no
  cadastro e na listagem).
- Alto acoplamento entre regra de negócio, acesso a dados e interface.
- Baixa testabilidade e dificuldade de troca de tecnologia.

> Esta decisão foi **substituída pelo [ADR-003](0003-arquitetura-em-camadas.md)**,
> que introduziu a arquitetura em camadas durante a refatoração.
