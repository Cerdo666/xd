import polars as pl
import streamlit as st
import altair as alt
import vega_datasets


@st.cache_data
def load_data():
    return vega_datasets.data.cars()

cars = load_data()

chart=alt.Chart(cars).mark_point().encode(
    x='Cylinders',
    y='Acceleration',
    color='Origin',
    tooltip=['Name', 'Origin'] # show Name and Origin in a tooltip
).interactive()


st.altair_chart(chart)