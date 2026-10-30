
"""
FUNCIONLAB
Módulo de análisis matemático.
"""

import numpy as np
import sympy as sp

from core.Proyecto_precalculo import (
    x,
    interpretar_funcion
)


# ==========================================
# CÁLCULO DEL DOMINIO
# ==========================================

def calcular_dominio(expresion):
    """Calcula el dominio real de una función."""

    try:
        dominio = sp.calculus.util.continuous_domain(
            expresion,
            x,
            sp.S.Reals
        )

        return dominio

    except (NotImplementedError, ValueError, TypeError):
        raise ValueError(
            "No se pudo determinar el dominio de esta función."
        )


# ==========================================
# CÁLCULO DEL CONTRADOMINIO
# ==========================================

def calcular_contradominio():
    """Devuelve el contradominio establecido por defecto."""

    return "R (números reales), por defecto"


# ==========================================
# ESTIMACIÓN DEL RECORRIDO
# ==========================================

def estimar_recorrido(
    expresion,
    dominio,
    xmin=-10,
    xmax=10,
    muestras=10001
):
    """Estima numéricamente el recorrido en un intervalo."""

    if xmin >= xmax:
        raise ValueError(
            "El límite inferior debe ser menor que el superior."
        )

    valores_x = np.linspace(
        xmin,
        xmax,
        muestras
    )

    funcion = sp.lambdify(
        x,
        expresion,
        modules=["numpy"]
    )

    with np.errstate(all="ignore"):

        try:
            valores_y = np.asarray(
                funcion(valores_x)
            )

        except Exception as error:
            raise ValueError(
                "No se pudo evaluar la función numéricamente."
            ) from error

    if valores_y.ndim == 0:
        valores_y = np.full(
            valores_x.shape,
            valores_y.item()
        )

    try:
        valores_y = np.broadcast_to(
            valores_y,
            valores_x.shape
        )

    except ValueError as error:
        raise ValueError(
            "La función no produjo resultados numéricos compatibles."
        ) from error

    if np.iscomplexobj(valores_y):

        reales = np.abs(
            np.imag(valores_y)
        ) < 1e-10

        valores_y = np.real(valores_y)

    else:

        reales = np.ones(
            valores_y.shape,
            dtype=bool
        )

    valores_y = np.asarray(
        valores_y,
        dtype=float
    )

    validos = reales & np.isfinite(valores_y)

    # Comprobar que los valores pertenezcan al dominio
    for indice in np.flatnonzero(validos):

        try:
            pertenece = dominio.contains(
                sp.Float(valores_x[indice])
            )

            if pertenece is sp.false:
                validos[indice] = False

        except (TypeError, ValueError, NotImplementedError):
            pass

    resultados = valores_y[validos]

    if resultados.size == 0:
        return (
            f"No se encontraron resultados reales "
            f"en [{xmin}, {xmax}]."
        )

    minimo = float(np.min(resultados))
    maximo = float(np.max(resultados))

    return (
        f"Aproximadamente desde {minimo:.6g} "
        f"hasta {maximo:.6g}, "
        f"analizando x entre {xmin} y {xmax}. "
        "Es una estimación numérica."
    )


# ==========================================
# ANÁLISIS GENERAL DE FUNCIONES
# ==========================================

def analizar_funcion(texto, xmin=-10, xmax=10):
    """Integra la interpretación y el análisis de una función."""

    expresion = interpretar_funcion(texto)

    dominio = calcular_dominio(expresion)

    return {

        # Expresión matemática
        "expresion_simbolica": expresion,

        # Expresión preparada para mostrar en Streamlit
        "expresion_latex": sp.latex(expresion),

        # Función en formato de texto
        "funcion": f"f(x) = {sp.sstr(expresion)}",

        # Resultados matemáticos
        "dominio": str(dominio),

        "contradominio": calcular_contradominio(),

        "recorrido_estimado": estimar_recorrido(
            expresion,
            dominio,
            xmin,
            xmax
        )
    }
