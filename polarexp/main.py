import polars as pl
import altair as alt
import streamlit as st

# Read CSV (está en el mismo directorio)
df = pl.read_csv("nombres_fechas.csv")

# Calculate age and count
df_count = (
    df.with_columns(
        pl.col("FechaNacimiento").str.to_date(format="%Y-%m-%d").alias("birth_date")
    )
    .with_columns(
        # Calculate age as of September 29, 2025
        ((pl.lit("2025-09-29").str.to_date() - pl.col("birth_date")).dt.total_days() // 365).alias("edad")
    )
    .group_by("edad")
    .agg(pl.len().alias("count"))
    .sort("edad")
)

# Bar chart: Count by age
chart = alt.Chart(df_count).mark_bar().encode(
    x=alt.X("count:Q", title="Cantidad"),
    y=alt.Y("edad:O", title="Edad"),
).properties(
    title="Personas por Edad"
)

# Display in Streamlit
st.altair_chart(chart, use_container_width=True)