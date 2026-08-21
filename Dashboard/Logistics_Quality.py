import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Logistics & Quality",
    page_icon="🚚",
    layout="wide"
)

DATA_FILE = Path(__file__).parents[1] / "supply_chain_data.csv"

df = pd.read_csv(DATA_FILE)

st.title("🚚 Logistics & Quality")
st.caption("Shipping, transportation and quality analysis")

modes = st.sidebar.multiselect(
    "Transportation Mode",
    sorted(df["Transportation modes"].unique()),
    default=sorted(df["Transportation modes"].unique())
)

carriers = st.sidebar.multiselect(
    "Shipping Carrier",
    sorted(df["Shipping carriers"].unique()),
    default=sorted(df["Shipping carriers"].unique())
)

df = df[
    df["Transportation modes"].isin(modes)
    &
    df["Shipping carriers"].isin(carriers)
]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average Shipping Time",
    f"{df['Shipping times'].mean():.1f} days"
)

col2.metric(
    "Average Shipping Cost",
    f"${df['Shipping costs'].mean():.2f}"
)

col3.metric(
    "Average Defect Rate",
    f"{df['Defect rates'].mean():.2f}%"
)

col4.metric(
    "Failed Inspections",
    (df["Inspection results"] == "Fail").sum()
)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    shipping = (
        df.groupby("Transportation modes", as_index=False)
        ["Shipping times"]
        .mean()
    )

    fig = px.bar(
        shipping,
        x="Transportation modes",
        y="Shipping times",
        title="Average Shipping Time"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    carrier = (
        df.groupby("Shipping carriers", as_index=False)
        ["Shipping costs"]
        .mean()
    )

    fig = px.bar(
        carrier,
        x="Shipping carriers",
        y="Shipping costs",
        title="Average Shipping Cost by Carrier"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    inspection = (
        df["Inspection results"]
        .value_counts()
        .reset_index()
    )

    inspection.columns = ["Result", "Count"]

    fig = px.pie(
        inspection,
        names="Result",
        values="Count",
        title="Inspection Results"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.scatter(
        df,
        x="Manufacturing costs",
        y="Defect rates",
        size="Production volumes",
        color="Product type",
        hover_data=["SKU", "Supplier name"],
        title="Manufacturing Cost vs Defect Rate"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.subheader("Route Performance")

route = (
    df.groupby("Routes", as_index=False)
    .agg(
        Average_Cost=("Costs", "mean"),
        Average_Shipping_Time=("Shipping times", "mean"),
        Average_Defect_Rate=("Defect rates", "mean")
    )
)

st.dataframe(
    route.round(2),
    use_container_width=True
)
