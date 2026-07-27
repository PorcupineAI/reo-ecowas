import streamlit as st
import pandas as pd
import plotly.express as px
import requests

API_BASE = "http://localhost:8000/api/v1"

def show():
    st.header("🗺️ Site Suitability Map")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        countries = ["All"] + ["Nigeria", "Benin", "Togo", "Ghana", "Côte d'Ivoire"]
        country = st.selectbox("Filter by Country", countries)
    
    with col2:
        min_score = st.slider("Minimum Suitability Score", 0, 100, 50)
    
    # Fetch data
    url = f"{API_BASE}/sites/top?limit=50"
    if country != "All":
        url += f"&country={country}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            sites = response.json()
            df = pd.DataFrame(sites)
            
            if not df.empty:
                # Map
                fig = px.scatter_mapbox(
                    df,
                    lat="latitude",
                    lon="longitude",
                    color="suitability_score",
                    size="suitability_score",
                    hover_name="name",
                    hover_data=["country", "solar_irradiance_kwh_m2", "grid_distance_km"],
                    color_continuous_scale="Viridis",
                    range_color=[0, 100],
                    zoom=5,
                    height=600
                )
                fig.update_layout(mapbox_style="open-street-map")
                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                st.plotly_chart(fig, use_container_width=True)
                
                # Data table
                st.subheader("📋 Site Rankings")
                st.dataframe(
                    df[["name", "country", "suitability_score", "solar_irradiance_kwh_m2", "grid_distance_km"]],
                    use_container_width=True
                )
            else:
                st.warning("No sites found matching filters")
        else:
            st.error("Failed to fetch data from API")
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to backend API. Please ensure the server is running.")
