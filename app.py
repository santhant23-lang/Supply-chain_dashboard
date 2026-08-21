import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Supply Chain Analytics",
    page_icon="📦",
    layout="wide"
)

DATA_FILE = Path(__file__).parent / "supply_chain_data.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)

    numeric_columns = [
        "Price",
        "Availability",
        "Number of products sold",
        "Revenue generated",
        "Stock levels",
        "Lead times",
        "Order quantities",
        "Shipping times",
        "Shipping costs",
        "Lead time",
        "Production volumes",
        "Manufacturing lead time",
        "Manufacturing costs",
        "Defect rates",
        "Costs"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


df = load_data()

st.sidebar.title("📦 Supply Chain Analytics")
st.sidebar.markdown("### Mini Project 2")
st.sidebar.markdown("Day 29 Dashboard")

st.title("📦 Supply Chain Analytics Dashboard")
st.subheader("Operational Overview")

st.write(
    "Interactive dashboard for analyzing revenue, inventory, "
    "suppliers, logistics, production and quality."
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"${df['Revenue generated'].sum():,.0f}"
)

col2.metric(
    "Units Sold",
    f"{df['Number of products sold'].sum():,.0f}"
)

col3.metric(
    "Average Defect Rate",
    f"{df['Defect rates'].mean():.2f}%"
)

col4.metric(
    "Total Supply Chain Cost",
    f"${df['Costs'].sum():,.0f}"
)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    product_revenue = (
        df.groupby("Product type", as_index=False)
        ["Revenue generated"]
        .sum()
    )

    fig = px.bar(
        product_revenue,
        x="Product type",
        y="Revenue generated",
        title="Revenue by Product Type"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    location_revenue = (
        df.groupby("Location", as_index=False)
        ["Revenue generated"]
        .sum()
    )

    fig = px.bar(
        location_revenue,
        x="Location",
        y="Revenue generated",
        title="Revenue by Location"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

st.subheader("Key Operational Metrics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Stock Level",
    f"{df['Stock levels'].mean():.1f}"
)

col2.metric(
    "Average Lead Time",
    f"{df['Lead time'].mean():.1f} days"
)

col3.metric(
    "Average Shipping Time",
    f"{df['Shipping times'].mean():.1f} days"
)

st.subheader("Dataset Preview")

st.dataframe(
    df.head(20),
    use_container_width=True
)