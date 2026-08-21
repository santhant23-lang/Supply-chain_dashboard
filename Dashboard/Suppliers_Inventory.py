import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Suppliers & Inventory",
    page_icon="🏭",
    layout="wide"
)

DATA_FILE = Path(__file__).parents[1] / "supply_chain_data.csv"

df = pd.read_csv(DATA_FILE)

st.title("🏭 Suppliers & Inventory")
st.caption("Supplier and inventory performance")

suppliers = st.sidebar.multiselect(
    "Supplier",
    sorted(df["Supplier name"].unique()),
    default=sorted(df["Supplier name"].unique())
)

df = df[df["Supplier name"].isin(suppliers)]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Suppliers",
    df["Supplier name"].nunique()
)

col2.metric(
    "Average Stock",
    f"{df['Stock levels'].mean():.1f}"
)

col3.metric(
    "Average Lead Time",
    f"{df['Lead time'].mean():.1f} days"
)

col4.metric(
    "Production Volume",
    f"{df['Production volumes'].sum():,.0f}"
)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    supplier_revenue = (
        df.groupby("Supplier name", as_index=False)
        ["Revenue generated"]
        .sum()
    )

    fig = px.bar(
        supplier_revenue,
        x="Supplier name",
        y="Revenue generated",
        title="Revenue by Supplier"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    stock = (
        df.groupby("Supplier name", as_index=False)
        ["Stock levels"]
        .mean()
    )

    fig = px.bar(
        stock,
        x="Supplier name",
        y="Stock levels",
        title="Average Stock Level by Supplier"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.subheader("Supplier Performance")

supplier_table = (
    df.groupby("Supplier name", as_index=False)
    .agg(
        SKUs=("SKU", "count"),
        Revenue=("Revenue generated", "sum"),
        Average_Stock=("Stock levels", "mean"),
        Average_Lead_Time=("Lead time", "mean"),
        Average_Defect_Rate=("Defect rates", "mean")
    )
)

st.dataframe(
    supplier_table.round(2),
    use_container_width=True
)
