
"""
FUNCIONLAB
Motor de interpretación matemática.
"""

import re
import sympy as sp

# Variable matemática principal
x = sp.Symbol("x", real=True)

# Funciones matemáticas permitidas
FUNCIONES = {
    "sqrt": sp.sqrt,
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "asin": sp.asin,
    "acos": sp.acos,
    "atan": sp.atan,
    "log": sp.log,
    "ln": sp.log,
    "exp": sp.exp,
    "abs": sp.Abs,
    "pi": sp.pi,
    "e": sp.E
}

NOMBRES_PERMITIDOS = {"x"} | set(FUNCIONES)


def formatear_expresion(texto):
    """Prepara la expresión para que SymPy pueda interpretarla."""

    texto = texto.strip()

    texto = re.sub(r"\bx([0-9]+)\b", r"x**\1", texto)
    texto = texto.replace("^", "**")

    if not re.fullmatch(
        r"[0-9A-Za-z_+\-*/().,^\s]+",
        texto
    ):
        raise ValueError(
            "La función contiene caracteres no permitidos."
        )

    texto = re.sub(
        r"(\d)\s*(?=[x(])",
        r"\1*",
        texto
    )

    texto = re.sub(
        r"([x)])\s*(?=[x(])",
        r"\1*",
        texto
    )

    return texto


def interpretar_funcion(texto):
    """Convierte el texto ingresado en una expresión simbólica."""

    texto_corregido = formatear_expresion(texto)

    if not texto_corregido:
        raise ValueError("Debes ingresar una función.")

    nombres = set(
        re.findall(r"[A-Za-z_]\w*", texto_corregido)
    )

    desconocidos = nombres - NOMBRES_PERMITIDOS

    if desconocidos:
        raise ValueError(
            "No se reconoce: " + ", ".join(sorted(desconocidos))
        )

    try:
        expresion = sp.sympify(
            texto_corregido,
            locals={
                "x": x,
                **FUNCIONES
            }
        )
    except Exception as error:
        raise ValueError(
            "La expresión matemática no es válida."
        ) from error

    if expresion.free_symbols - {x}:
        raise ValueError(
            "Solo se permite utilizar la variable x."
        )

    if expresion.has(sp.nan, sp.zoo, sp.S.ComplexInfinity):
        raise ValueError(
            "La expresión contiene valores no definidos."
        )

    return expresion
