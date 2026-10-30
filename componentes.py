
"""
FUNCIONLAB
Componentes reutilizables de la interfaz.
"""

import streamlit as st


def mostrar_encabezado():
    """Muestra el encabezado principal."""

    st.title("📈 FUNCIONLAB")

    st.subheader(
        "Análisis matemático y graficadora de funciones"
    )

    st.write(
        """
        Bienvenido a FUNCIONLAB. Ingresa una función matemática
        para analizar su dominio, contradominio, recorrido
        y representación gráfica.
        """
    )


def mostrar_resultados(resultado):
    """Muestra los resultados del análisis matemático."""

    st.divider()
    st.header("Resultados matemáticos")

    st.subheader("Función ingresada")

    st.latex(
        resultado["expresion_latex"]
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Dominio**")
        st.write(resultado["dominio"])

    with col2:
        st.markdown("**Contradominio**")
        st.write(resultado["contradominio"])

    st.markdown("**Recorrido estimado**")
    st.write(resultado["recorrido_estimado"])

    st.caption(
        "El recorrido mostrado es una estimación numérica "
        "dentro del intervalo seleccionado; no necesariamente "
        "representa el recorrido exacto."
    )


def mostrar_pie():
    """Muestra el pie de página."""

    st.divider()

    st.caption(
        "FUNCIONLAB | Proyecto académico de Precálculo"
    )
