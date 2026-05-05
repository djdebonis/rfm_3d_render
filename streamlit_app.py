import streamlit as st
import pandas as pd
import plotly.express as px

st.title("3D RFM Cohort Bubble Plot")

# Change this to your local CSV filename/path
file_path = "full_rfm_data.csv"

customer_summary = pd.read_csv(file_path)

required_cols = ["recency_score", "frequency_score", "monetary_score"]

for col in required_cols:
    customer_summary[col] = pd.to_numeric(customer_summary[col], errors="coerce")

customer_summary = customer_summary.dropna(subset=required_cols)

if "rfm_code" not in customer_summary.columns:
    customer_summary["rfm_code"] = (
        customer_summary["recency_score"].astype(int).astype(str) +
        customer_summary["frequency_score"].astype(int).astype(str) +
        customer_summary["monetary_score"].astype(int).astype(str)
    )

rfm_bubbles = (
    customer_summary
    .groupby(["rfm_code", "recency_score", "frequency_score", "monetary_score"])
    .size()
    .reset_index(name="num_customers")
)

fig = px.scatter_3d(
    rfm_bubbles,
    x="recency_score",
    y="frequency_score",
    z="monetary_score",
    size="num_customers",
    color="rfm_code",
    hover_name="rfm_code",
    size_max=55,
    opacity=0.75
)

fig.update_layout(
    title="3D RFM Cohort Bubble Plot",
    scene=dict(
        xaxis_title="Recency Score",
        yaxis_title="Frequency Score",
        zaxis_title="Monetary Score"
    )
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(
    rfm_bubbles.sort_values("num_customers", ascending=False)
)