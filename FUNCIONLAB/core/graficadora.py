
"""
FUNCIONLAB
Módulo de representación gráfica.
"""

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

from core.Proyecto_precalculo import x


def graficar_funcion(
    expresion,
    xmin=-10,
    xmax=10,
    muestras=2000
):
    """Genera la gráfica de una función matemática."""

    if xmin >= xmax:
        raise ValueError(
            "El límite inferior debe ser menor que el superior."
        )

    valores_x = np.linspace(xmin, xmax, muestras)

    funcion = sp.lambdify(
        x,
        expresion,
        modules=["numpy"]
    )

    with np.errstate(all="ignore"):
        try:
            valores_y = funcion(valores_x)

            if np.isscalar(valores_y):
                valores_y = np.full(
                    valores_x.shape,
                    valores_y,
                    dtype=float
                )
            else:
                valores_y = np.asarray(
                    valores_y,
                    dtype=complex
                )

        except Exception as error:
            raise ValueError(
                "No se pudo generar la gráfica."
            ) from error

    reales = np.abs(np.imag(valores_y)) < 1e-10

    valores_y = np.where(
        reales,
        np.real(valores_y),
        np.nan
    )

    # Evitar unir puntos separados por saltos bruscos
    diferencias = np.abs(np.diff(valores_y))

    asintotas = np.where(diferencias > 20)[0]

    for indice in asintotas:
        valores_y[indice] = np.nan

    figura, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        valores_x,
        valores_y,
        label=f"f(x) = {sp.sstr(expresion)}",
        color="#0052cc",
        linewidth=2
    )

    ax.axhline(0, color="black", linewidth=1.2)
    ax.axvline(0, color="black", linewidth=1.2)

    ax.set_title(
        f"Gráfica de f(x) = {sp.sstr(expresion)}",
        fontsize=14
    )

    ax.set_xlabel("Eje X (Dominio)")
    ax.set_ylabel("Eje Y (Recorrido)")

    ax.grid(
        color="gray",
        linestyle="--",
        linewidth=0.5,
        alpha=0.7
    )

    ax.legend(loc="upper right")
    ax.set_xlim(xmin, xmax)

    # Ajustar el eje Y según los valores visibles
    validos = valores_y[np.isfinite(valores_y)]

    if validos.size > 0:
        minimo = float(np.min(validos))
        maximo = float(np.max(validos))

        margen = max((maximo - minimo) * 0.1, 1)

        ax.set_ylim(
            minimo - margen,
            maximo + margen
        )

    figura.tight_layout()

    return figura
