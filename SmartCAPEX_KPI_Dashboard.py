import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="SmartCAPEX KPI Dashboard")

st.title("Infrastructure Health Overview")

# File uploader
uploaded_file = st.sidebar.file_uploader("Upload Asset CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.warning("Please upload a CSV file to continue.")
    st.stop()

# Asset type filter
asset_types = df["Asset Type"].dropna().unique()
selected_type = st.sidebar.selectbox("Select Asset Type", ["All"] + list(asset_types))

if selected_type != "All":
    df_filtered = df[df["Asset Type"] == selected_type]
else:
    df_filtered = df

# Convert Risk to numeric if needed
df_filtered["Risk"] = pd.to_numeric(df_filtered["Risk"], errors="coerce")

# KPI metrics
avg_condition = round(df_filtered["Condition"].mean(), 2)
avg_risk = round(df_filtered["Risk"].mean(), 2)
total_assets = df_filtered.shape[0]
below_threshold = df_filtered[df_filtered["Condition"] < 3.0].shape[0]

# Display visuals
col1, col2 = st.columns(2)

with col1:
    fig_bar = go.Figure(go.Bar(
        x=["Avg. Condition", "Avg. Risk", "Total Assets", "Below Threshold"],
        y=[avg_condition, avg_risk, total_assets, below_threshold],
        marker_color=["darkred", "orange", "gray", "red"]
    ))
    fig_bar.update_layout(title="Asset KPI Summary", height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_risk,
        title={'text': "Average Risk Level"},
        gauge={
            'axis': {'range': [0, 5]},
            'bar': {'color': "orange"},
            'steps': [
                {'range': [0, 2], 'color': "green"},
                {'range': [2, 4], 'color': "yellow"},
                {'range': [4, 5], 'color': "red"},
            ]
        }
    ))
    fig_gauge.update_layout(height=400)
    st.plotly_chart(fig_gauge, use_container_width=True)

st.caption("SmartCAPEX DT-lite KPI Module")
