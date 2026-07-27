import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from pages import map_view, optimization, regulatory_matrix, carbon_finance

st.set_page_config(
    page_title="REO-ECOWAS Dashboard",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ REO-ECOWAS: Regional Energy Orchestration Platform")
st.caption("ECOWAS Renewable Energy & Energy Efficiency Decision Support Tool")

# Sidebar navigation
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Map View", "⚙️ Optimization", "📊 Regulatory Matrix", "🌿 Carbon Finance"]
)

if page == "🏠 Map View":
    map_view.show()
elif page == "⚙️ Optimization":
    optimization.show()
elif page == "📊 Regulatory Matrix":
    regulatory_matrix.show()
elif page == "🌿 Carbon Finance":
    carbon_finance.show()
