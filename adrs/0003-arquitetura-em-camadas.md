# ADR-003: Adotar arquitetura de monolito modular em camadas

- **Status:** Accepted
- **Data:** 2026-05-26
- **Decisores:** equipe do projeto
- **Supersedes:** [ADR-002](0002-monolito-procedural.md)

## Contexto

O sistema é pequeno, operado por um único tipo de usuário e implantado em uma única
máquina. Era necessário decidir entre um monolito (clássico ou modular) e
microsserviços, considerando os atributos de qualidade priorizados
(manutenibilidade, confiabilidade e capacidade de interação) e o tamanho da equipe.
A estrutura procedural anterior ([ADR-002](0002-monolito-procedural.md)) mostrou-se
difícil de manter e testar.

## Decisão

Adotar um **monolito modular**, organizado internamente em camadas — apresentação
(`src/presentation`), serviço (`src/service`), domínio (`src/domain`) e persistência
(`src/repository`, `src/data`) — com fronteiras claras e dependências
unidirecionais entre os módulos.

## Consequências

### Benefícios
- Simplicidade de implantação e depuração; baixo custo operacional.
- Boa manutenibilidade pela separação de responsabilidades.
- Habilita testes por camada (o serviço é testável sem banco real).

### Custos
- Menor independência de escalonamento entre partes do sistema — limitação
  aceitável, pois não há requisito de escala que justifique microsserviços.
- Mais arquivos e indireção do que a abordagem procedural.
