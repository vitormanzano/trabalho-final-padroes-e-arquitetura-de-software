"""Validação de dados de produto.

Concentra todas as regras de validação em um único módulo de domínio.
"""

from dataclasses import dataclass


@dataclass
class ErroValidacao(Exception):
    campo: str
    mensagem: str

    def __str__(self) -> str:
        return f"{self.campo}: {self.mensagem}"


def validar_produto(
    id_produto: int,
    nome: str,
    descricao: str,
    custo_produto: float,
    custo_fixo: float,
    comissao: float,
    imposto: float,
    margem_lucro: float,
) -> None:
    """Lança ErroValidacao se qualquer campo violar as regras de negócio."""
    if id_produto <= 0:
        raise ErroValidacao("id_produto", "Deve ser um inteiro positivo.")

    if not nome or not nome.strip():
        raise ErroValidacao("nome", "Não pode ser vazio.")

    if not descricao or not descricao.strip():
        raise ErroValidacao("descricao", "Não pode ser vazia.")

    if custo_produto < 0:
        raise ErroValidacao("custo_produto", "Não pode ser negativo.")

    for campo, valor in [
        ("custo_fixo", custo_fixo),
        ("comissao", comissao),
        ("imposto", imposto),
    ]:
        if not (0 <= valor < 100):
            raise ErroValidacao(campo, "Deve estar entre 0 e 100.")

    soma = custo_fixo + comissao + imposto + margem_lucro
    if soma >= 100:
        raise ErroValidacao(
            "margem_lucro",
            f"A soma dos percentuais ({soma:.2f}%) deve ser menor que 100.",
        )
