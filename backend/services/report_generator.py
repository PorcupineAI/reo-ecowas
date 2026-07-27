import pandas as pd
from io import BytesIO
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from models import Site, RegulatoryScore, OptimizationRun


class ReportGenerator:
    """Generate downloadable Excel/CSV reports for ECOWAS working groups."""

    @staticmethod
    def generate_full_excel_report(db: Session, country: Optional[str] = None) -> BytesIO:
        """
        Create a multi-sheet Excel workbook with:
        - Sites summary
        - Regulatory matrix
        - Optimization results
        - Investment pipeline
        """
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Sheet 1: Sites
            query = db.query(Site)
            if country:
                query = query.filter(Site.country == country)
            sites = query.all()
            sites_data = [{
                "Name": s.name,
                "Country": s.country,
                "Latitude": s.latitude,
                "Longitude": s.longitude,
                "Population": s.population,
                "Suitability Score": s.suitability_score,
                "Solar Irradiance (kWh/m²)": s.solar_irradiance_kwh_m2,
                "Grid Distance (km)": s.grid_distance_km,
                "Transmission Loss (%)": s.transmission_loss_percent,
                "Diesel (L/day)": s.current_diesel_consumption_l_per_day,
                "Load (kW)": s.estimated_load_kw,
                "Productive Use": s.productive_use_type
            } for s in sites]
            df_sites = pd.DataFrame(sites_data)
            df_sites.to_excel(writer, sheet_name="Sites", index=False)

            # Sheet 2: Regulatory Matrix
            regs = db.query(RegulatoryScore).all()
            reg_data = [{
                "Country": r.country,
                "Tariff Approval": r.tariff_approval_time_score,
                "Import Duty": r.import_duty_on_solar_score,
                "Local Content": r.local_content_requirement_score,
                "Land Acquisition": r.land_acquisition_score,
                "Grid Policy": r.grid_connection_policy_score,
                "Friction Score": r.overall_regulatory_friction_score
            } for r in regs]
            df_reg = pd.DataFrame(reg_data)
            df_reg.to_excel(writer, sheet_name="Regulatory", index=False)

            # Sheet 3: Optimization Results
            opt_runs = db.query(OptimizationRun).join(Site).all()
            opt_data = [{
                "Site": o.site.name,
                "Country": o.site.country,
                "Solar (kW)": o.solar_capacity_kw,
                "Battery (kWh)": o.battery_capacity_kwh,
                "Diesel Saved (L/day)": o.predicted_diesel_savings_l_per_day,
                "CO₂ Reduced (tons/yr)": o.predicted_co2_reduction_tons_per_year,
                "Cost Savings ($/yr)": o.predicted_cost_savings_usd_per_year,
                "Carbon Revenue ($/yr)": o.carbon_credit_revenue_usd_per_year,
                "Payback (years)": o.payback_period_years,
                "Run Date": o.run_date.strftime("%Y-%m-%d")
            } for o in opt_runs]
            df_opt = pd.DataFrame(opt_data)
            df_opt.to_excel(writer, sheet_name="Optimization", index=False)

            # Sheet 4: Summary Dashboard
            summary = {
                "Metric": [
                    "Total Sites",
                    "Average Suitability",
                    "Total CO₂ Reduction (tons/yr)",
                    "Total Cost Savings ($/yr)",
                    "Total Carbon Revenue ($/yr)",
                    "Report Generated"
                ],
                "Value": [
                    len(sites),
                    round(df_sites["Suitability Score"].mean(), 1) if not df_sites.empty else 0,
                    round(df_opt["CO₂ Reduced (tons/yr)"].sum(), 2) if not df_opt.empty else 0,
                    round(df_opt["Cost Savings ($/yr)"].sum(), 0) if not df_opt.empty else 0,
                    round(df_opt["Carbon Revenue ($/yr)"].sum(), 0) if not df_opt.empty else 0,
                    datetime.now().strftime("%Y-%m-%d %H:%M UTC")
                ]
            }
            df_summary = pd.DataFrame(summary)
            df_summary.to_excel(writer, sheet_name="Dashboard", index=False)

        output.seek(0)
        return output
