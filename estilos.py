
"""
FUNCIONLAB
Estilos visuales de la aplicación.
"""

import streamlit as st


def aplicar_estilos():
    """Aplica el diseño visual general de FUNCIONLAB."""

    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0B1120;
            color: #F1F5F9;
        }

        h1, h2, h3 {
            color: #38BDF8 !important;
        }

        p, label, span {
            color: #E2E8F0;
        }

        .stTextInput input,
        .stNumberInput input {
            background-color: #1E293B;
            color: white;
            border-radius: 8px;
        }

        .stButton button,
        .stFormSubmitButton button {
            background-color: #0284C7;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
        }

        .stButton button:hover,
        .stFormSubmitButton button:hover {
            background-color: #0369A1;
            color: white;
        }

        [data-testid="stMetric"] {
            background-color: #1E293B;
            padding: 15px;
            border-radius: 10px;
        }

        hr {
            border-color: #334155;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
