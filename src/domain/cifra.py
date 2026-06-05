"""Cifra de substituição usada para ofuscar descrições de produtos.

Encapsula a lógica de criptografia/descriptografia que estava em funções
procedurais soltas no código legado.
"""

_TABELA = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
_CHAVE_CIFRA = [4, 3, 1, 2]
_CHAVE_DECIFRA = [42, -63, -21, 84]


def _texto_para_numeros(texto: str) -> list[int]:
    resultado = []
    for caractere in texto:
        if caractere not in _TABELA:
            raise ValueError(f"Caractere inválido para cifra: '{caractere}'")
        resultado.append(_TABELA.index(caractere) + 1)
    return resultado


def _aplicar_matriz(numeros: list[int], chave: list[int]) -> list[int]:
    resultado = []
    for i in range(0, 3, 2):
        for k in range(0, len(numeros), 2):
            valor = chave[i] * numeros[k] + chave[i + 1] * numeros[k + 1]
            resultado.append(valor % 26)
    return resultado


def _numeros_para_texto(primeira: list[int], segunda: list[int]) -> str:
    texto = ""
    for a, b in zip(primeira, segunda):
        texto += _TABELA[a - 1] + _TABELA[b - 1]
    return texto


def criptografar(texto: str) -> str:
    """Cifra um texto usando a cifra de substituição do domínio."""
    if not texto:
        return ""
    texto = texto.upper().replace(" ", "")
    if len(texto) % 2 == 1:
        texto += texto[-1]
    numeros = _texto_para_numeros(texto)
    cifrados = _aplicar_matriz(numeros, _CHAVE_CIFRA)
    metade = len(numeros) // 2
    return _numeros_para_texto(cifrados[:metade], cifrados[metade:])


def descriptografar(texto: str) -> str:
    """Decifra um texto previamente cifrado por ``criptografar``."""
    texto = texto.upper().replace(" ", "")
    numeros = []
    for caractere in texto:
        # O legado usa index+1 com Z (índice 25) virando 0 — mesmo esquema da cifra
        valor = _TABELA.index(caractere) + 1
        numeros.append(valor if valor != 26 else 0)
    decifrados = _aplicar_matriz(numeros, _CHAVE_DECIFRA)
    metade = len(decifrados) // 2
    return _numeros_para_texto(decifrados[:metade], decifrados[metade:])
