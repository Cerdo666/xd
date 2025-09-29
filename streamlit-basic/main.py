import streamlit as st
from streamlit_option_menu import option_menu
import polars as pl
import altair as alt
import requests

st.set_page_config(page_title="Esperanza de vida y Fertilidad", layout="wide")

# --- Año seleccionado ---
year = 2000  # puedes cambiar el año aquí fácilmente

# --- Sidebar menu ---
with st.sidebar:
    selected = option_menu(
        "Menú principal",
        ["Esperanza de vida", "Fertilidad"],
        icons=['heart-pulse', 'baby'],
        menu_icon="cast",
        default_index=0
    )

# --- Dataset ---
url = "https://raw.githubusercontent.com/vega/vega-datasets/main/data/countries.json"
data = requests.get(url).json()
df = pl.DataFrame(data)

# Filtrar solo año seleccionado
df_year = df.filter(pl.col("year") == year).select(["country", "life_expect", "fertility"])
df_year_pd = df_year.to_pandas()

# --- Página: Esperanza de vida ---
if selected == "Esperanza de vida":
    st.title(f"📊 Esperanza de vida en el año {year}")

    chart = (
        alt.Chart(df_year_pd)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
        .encode(
            x=alt.X("country:N", sort="y", title="País"),  # orden ascendente
            y=alt.Y("life_expect:Q", title="Esperanza de vida (años)"),
            color=alt.Color("life_expect:Q", scale=alt.Scale(scheme="blues"), legend=None),
            tooltip=["country", "life_expect"]
        )
        .properties(width=800, height=400)
    )

    st.altair_chart(chart, use_container_width=True)

# --- Página: Fertilidad ---
elif selected == "Fertilidad":
    st.title(f"👶 Fertilidad en el año {year}")

    chart = (
        alt.Chart(df_year_pd)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
        .encode(
            x=alt.X("country:N", sort="y", title="País"),  # orden ascendente
            y=alt.Y("fertility:Q", title="Fertilidad (hijos por mujer)"),
            color=alt.Color("fertility:Q", scale=alt.Scale(scheme="oranges"), legend=None),
            tooltip=["country", "fertility"]
        )
        .properties(width=800, height=400)
    )

    st.altair_chart(chart, use_container_width=True)
