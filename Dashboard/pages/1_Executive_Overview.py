import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Executive Overview",
    page_icon="📊",
    layout="wide"
)

DATA_FILE = Path(__file__).parents[1] / "supply_chain_data.csv"

df = pd.read_csv(DATA_FILE)

st.title("📊 Executive Overview")
st.caption("Supply Chain Business Performance")

st.sidebar.header("Filters")

product_types = st.sidebar.multiselect(
    "Product Type",
    sorted(df["Product type"].unique()),
    default=sorted(df["Product type"].unique())
)

locations = st.sidebar.multiselect(
    "Location",
    sorted(df["Location"].unique()),
    default=sorted(df["Location"].unique())
)

df = df[
    df["Product type"].isin(product_types)
    &
    df["Location"].isin(locations)
]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Revenue",
    f"${df['Revenue generated'].sum():,.0f}"
)

col2.metric(
    "Units Sold",
    f"{df['Number of products sold'].sum():,.0f}"
)

col3.metric(
    "Average Price",
    f"${df['Price'].mean():,.2f}"
)

col4.metric(
    "Total Cost",
    f"${df['Costs'].sum():,.0f}"
)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    revenue = (
        df.groupby("Product type", as_index=False)
        ["Revenue generated"]
        .sum()
    )

    fig = px.bar(
        revenue,
        x="Product type",
        y="Revenue generated",
        title="Revenue by Product Type"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    location = (
        df.groupby("Location", as_index=False)
        ["Revenue generated"]
        .sum()
    )

    fig = px.pie(
        location,
        names="Location",
        values="Revenue generated",
        title="Revenue Share by Location"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.subheader("Top 10 SKUs by Revenue")

top_skus = (
    df.groupby("SKU", as_index=False)
    ["Revenue generated"]
    .sum()
    .sort_values(
        "Revenue generated",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    top_skus,
    x="Revenue generated",
    y="SKU",
    orientation="h",
    title="Top 10 SKUs"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
