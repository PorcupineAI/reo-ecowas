import streamlit as st
import pandas as pd
import plotly.express as px
import requests

API_BASE = "http://localhost:8000/api/v1"

def show():
    st.header("📊 Regulatory Friction Matrix")
    st.markdown("""
    **Lower friction = easier deployment.**  
    Scores range 1-5 (5 = most favorable). Adjust scores to simulate policy changes.
    """)
    
    try:
        response = requests.get(f"{API_BASE}/regulatory/")
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            
            # Display map
            fig = px.choropleth(
                df,
                locations="country",
                locationmode="country names",
                color="overall_regulatory_friction_score",
                hover_name="country",
                range_color=[0, 4],
                color_continuous_scale="RdYlGn_r",  # Green = low friction
                title="Regulatory Friction Score (Lower is Better)"
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Editable table
            st.subheader("✏️ Edit Country Scores")
            for idx, row in df.iterrows():
                with st.expander(f"{row['country']} (Friction: {row['overall_regulatory_friction_score']})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        tariff = st.slider(f"Tariff Approval Time", 1, 5, row['tariff_approval_time_score'], key=f"tariff_{row['country']}")
                        import_duty = st.slider(f"Import Duty on Solar", 1, 5, row['import_duty_on_solar_score'], key=f"import_{row['country']}")
                    with col2:
                        local_content = st.slider(f"Local Content Req", 1, 5, row['local_content_requirement_score'], key=f"local_{row['country']}")
                        land = st.slider(f"Land Acquisition", 1, 5, row['land_acquisition_score'], key=f"land_{row['country']}")
                    
                    if st.button(f"Update {row['country']}", key=f"update_{row['country']}"):
                        update_data = {
                            "tariff_approval_time_score": tariff,
                            "import_duty_on_solar_score": import_duty,
                            "local_content_requirement_score": local_content,
                            "land_acquisition_score": land,
                            "grid_connection_policy_score": row['grid_connection_policy_score']  # keep existing
                        }
                        put_resp = requests.put(f"{API_BASE}/regulatory/{row['country']}", json=update_data)
                        if put_resp.status_code == 200:
                            st.success(f"✅ {row['country']} updated!")
                            st.rerun()
                        else:
                            st.error("Update failed.")
        else:
            st.warning("No regulatory data found. Please run seed script.")
    except Exception as e:
        st.error(f"Error: {e}")
