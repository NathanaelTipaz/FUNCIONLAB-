
"""
FUNCIONLAB
Aplicación web de análisis matemático y graficación.
"""

import streamlit as st
import sympy as sp
import matplotlib.pyplot as plt

from core.analisis import analizar_funcion
from core.graficadora import graficar_funcion

from ui.estilos import aplicar_estilos

from ui.componentes import (
    mostrar_encabezado,
    mostrar_resultados,
    mostrar_pie
)


# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================

st.set_page_config(
    page_title="FUNCIONLAB",
    page_icon="📈",
    layout="wide"
)

# Aplicar diseño visual
aplicar_estilos()


# ==========================================
# ENCABEZADO
# ==========================================

mostrar_encabezado()

st.info(
    "Ejemplos: x^2, 2x+3, 1/x, sqrt(x), "
    "sin(x), cos(x), log(x)"
)


# ==========================================
# FORMULARIO DE ANÁLISIS
# ==========================================

with st.form("formulario_funcion"):

    entrada = st.text_input(
        "Ingresa la función f(x):",
        value="x^2",
        placeholder="Ejemplo: x^2 - 4"
    )

    col1, col2 = st.columns(2)

    with col1:
        xmin = st.number_input(
            "Valor mínimo de x",
            value=-10.0
        )

    with col2:
        xmax = st.number_input(
            "Valor máximo de x",
            value=10.0
        )

    analizar = st.form_submit_button(
        "Analizar función",
        use_container_width=True
    )


# ==========================================
# PROCESAMIENTO DE RESULTADOS
# ==========================================

if analizar:

    try:

        if xmin >= xmax:
            raise ValueError(
                "El valor mínimo debe ser menor que el máximo."
            )

        resultado = analizar_funcion(
            entrada,
            xmin,
            xmax
        )

        st.success(
            "¡Análisis realizado correctamente!"
        )

        # Mostrar resultados
        mostrar_resultados(resultado)

        # Mostrar gráfica
        st.divider()

        st.header("Representación gráfica")

        figura = graficar_funcion(
            resultado["expresion_simbolica"],
            xmin,
            xmax
        )

        st.pyplot(
            figura,
            use_container_width=True
        )

        plt.close(figura)

    except ValueError as error:

        st.error(str(error))

    except Exception as error:

        st.error(
            f"Ocurrió un error inesperado: {error}"
        )


# ==========================================
# PIE DE PÁGINA
# ==========================================

mostrar_pie()
