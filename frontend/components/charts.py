import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_suitability_map(df: pd.DataFrame) -> go.Figure:
    """Create an interactive suitability score map."""
    if df.empty:
        return go.Figure()
    
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
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    return fig

def create_optimization_bar_chart(metrics: dict) -> go.Figure:
    """Bar chart for optimization results."""
    if not metrics:
        return go.Figure()
    
    fig = go.Figure(data=[
        go.Bar(
            x=["Diesel Savings (L/day)", "CO₂ Reduction (tons/yr)", 
               "Cost Savings ($/yr)", "Carbon Revenue ($/yr)"],
            y=[metrics.get("diesel_savings_l_per_day", 0),
               metrics.get("co2_reduction_tons_per_year", 0),
               metrics.get("cost_savings_usd_per_year", 0),
               metrics.get("carbon_credit_revenue_usd_per_year", 0)],
            marker_color=["#2E86AB", "#A23B72", "#F18F01", "#73AB84"]
        )
    ])
    fig.update_layout(
        title="Optimization Impact Summary",
        xaxis_title="Metric",
        yaxis_title="Value",
        height=400
    )
    return fig

def create_regulatory_friction_heatmap(df: pd.DataFrame) -> go.Figure:
    """Heatmap of regulatory friction scores."""
    if df.empty:
        return go.Figure()
    
    # Pivot for heatmap
    pivot_df = df.set_index("country")[["tariff_approval_time_score", "import_duty_on_solar_score", 
                                        "local_content_requirement_score", "land_acquisition_score",
                                        "grid_connection_policy_score"]]
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns.str.replace("_", " ").str.title(),
        y=pivot_df.index,
        colorscale="RdYlGn",
        text=pivot_df.values,
        texttemplate="%{text}",
        textfont={"size": 10},
        hoverongaps=False
    ))
    fig.update_layout(
        title="Regulatory Scores by Country (5 = Best)",
        height=500,
        xaxis={"side": "bottom"}
    )
    return fig

def create_carbon_credit_timeline(historical_data: list) -> go.Figure:
    """Line chart for carbon credit accumulation over time."""
    if not historical_data:
        return go.Figure()
    
    df = pd.DataFrame(historical_data)
    fig = px.line(
        df,
        x="date",
        y="cumulative_co2_reduction",
        title="Cumulative CO₂ Reduction (tons)",
        labels={"date": "Date", "cumulative_co2_reduction": "Tons CO₂"}
    )
    fig.update_layout(height=400)
    return fig
