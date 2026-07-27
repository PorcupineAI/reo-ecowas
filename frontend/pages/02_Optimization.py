import streamlit as st
import pandas as pd
import plotly.express as px
import requests

API_BASE = "http://localhost:8000/api/v1"

def show():
    st.header("⚙️ Site Optimization Tool")
    st.markdown("""
    **Simulate the impact of adding solar + battery storage to any site.**
    The optimizer minimizes diesel consumption and maximizes cost savings.
    """)
    
    # Site selection
    try:
        response = requests.get(f"{API_BASE}/sites/top?limit=20")
        if response.status_code == 200:
            sites = response.json()
            site_names = {s["name"]: s["id"] for s in sites}
            selected_name = st.selectbox("Select Site", list(site_names.keys()))
            site_id = site_names[selected_name]
            
            # Find site data
            site_data = next(s for s in sites if s["id"] == site_id)
            
            # Input parameters
            col1, col2 = st.columns(2)
            with col1:
                solar_kw = st.number_input("Solar Capacity (kW)", min_value=1, max_value=500, value=50)
            with col2:
                battery_kwh = st.number_input("Battery Capacity (kWh)", min_value=10, max_value=1000, value=100)
            
            if st.button("🚀 Run Optimization", type="primary"):
                with st.spinner("Running optimization..."):
                    opt_response = requests.post(
                        f"{API_BASE}/optimize/",
                        json={"site_id": site_id, "solar_capacity_kw": solar_kw, "battery_capacity_kwh": battery_kwh}
                    )
                    
                    if opt_response.status_code == 200:
                        result = opt_response.json()
                        
                        # Display results
                        st.success("✅ Optimization complete!")
                        
                        metrics = st.columns(4)
                        with metrics[0]:
                            st.metric("Diesel Savings", f"{result['predicted_diesel_savings_l_per_day']:.1f} L/day")
                        with metrics[1]:
                            st.metric("CO₂ Reduction", f"{result['predicted_co2_reduction_tons_per_year']:.1f} tons/yr")
                        with metrics[2]:
                            st.metric("Cost Savings", f"${result['predicted_cost_savings_usd_per_year']:,.0f}/yr")
                        with metrics[3]:
                            st.metric("Carbon Credit Revenue", f"${result['carbon_credit_revenue_usd_per_year']:,.0f}/yr")
                        
                        # Payback visualization
                        st.subheader("📈 Investment Analysis")
                        capex = solar_kw * 800 + battery_kwh * 300  # Rough estimate
                        annual_savings = result['predicted_cost_savings_usd_per_year'] + result['carbon_credit_revenue_usd_per_year']
                        payback = capex / annual_savings if annual_savings > 0 else 0
                        
                        st.info(f"**Estimated CAPEX:** ${capex:,.0f} | **Annual Savings:** ${annual_savings:,.0f} | **Payback Period:** {payback:.1f} years")
                    else:
                        st.error("Optimization failed")
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to backend API. Please ensure the server is running.
