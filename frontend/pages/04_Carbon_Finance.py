import streamlit as st
import pandas as pd
import plotly.express as px
import requests

API_BASE = "http://localhost:8000/api/v1"

def show():
    st.header("🌿 Carbon Finance & MRV Dashboard")
    st.markdown("""
    **Monitor and verify avoided emissions.**  
    This module estimates carbon credit revenue based on diesel displacement.
    """)
    
    # Manual MRV Calculator
    st.subheader("🧮 Quick MRV Estimator")
    col1, col2 = st.columns(2)
    with col1:
        baseline_diesel = st.number_input("Baseline Diesel (L/day)", min_value=0.0, value=50.0)
    with col2:
        optimized_diesel = st.number_input("Optimized Diesel (L/day)", min_value=0.0, value=18.0)
    
    if st.button("Calculate Carbon Credits"):
        # Emission factors
        DIESEL_EF = 2.68  # kg CO2 per liter
        carbon_price = 35.0  # USD per ton
        
        avoided_l_per_day = baseline_diesel - optimized_diesel
        avoided_co2_kg_per_day = avoided_l_per_day * DIESEL_EF
        avoided_co2_tons_per_year = (avoided_co2_kg_per_day * 365) / 1000
        revenue = avoided_co2_tons_per_year * carbon_price
        
        st.success(f"**Avoided Emissions:** {avoided_co2_tons_per_year:.2f} tons CO2/year")
        st.success(f"**Estimated Carbon Revenue:** ${revenue:,.2f}/year")
        
        # Display MRV compliance checklist
        st.info("""
        **MRV Verification Checklist (Gold Standard):**
        - ✅ Baseline established (historical diesel records)
        - ✅ Metering installed (kWh +/- 2% accuracy)
        - ✅ Third-party audit scheduled
        - ⚠️ Pending: Sustainable Development Goal (SDG) co-benefits report
        """)
    
    # Fetch actual data from API
    st.subheader("📈 Project-Level MRV")
    try:
        resp = requests.get(f"{API_BASE}/reports/summary")
        if resp.status_code == 200:
            data = resp.json()
            opt = data["optimization_impact"]
            st.metric("Total CO₂ Reduction", f"{opt['total_co2_reduction_tons_per_year']} tons/yr")
            st.metric("Total Cost Savings", f"${opt['total_cost_savings_usd_per_year']:,.0f}")
            
            # Chart
            df_chart = pd.DataFrame([{
                "Metric": "CO2 Reduction",
                "Value": opt['total_co2_reduction_tons_per_year']
            }, {
                "Metric": "Cost Savings ($k)",
                "Value": opt['total_cost_savings_usd_per_year'] / 1000
            }])
            fig = px.bar(df_chart, x="Metric", y="Value", text_auto=True)
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning("Connect to backend for live MRV data.")
