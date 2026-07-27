from typing import Dict
from config import settings

class CarbonFinanceCalculator:
    """
    Calculate carbon credit revenue and MRV metrics.
    Aligned with Gold Standard and Verra methodologies.
    """
    
    # Emission factors (kg CO2 per unit)
    DIESEL_EF = 2.68  # kg CO2 per liter
    GRID_EF = 0.45    # kg CO2 per kWh (West Africa average)
    
    @classmethod
    def calculate_avoided_emissions(
        cls, 
        baseline_diesel_l_per_day: float,
        optimized_diesel_l_per_day: float,
        baseline_grid_kwh_per_day: float = 0,
        optimized_grid_kwh_per_day: float = 0
    ) -> Dict:
        """
        Calculate CO2 avoided vs baseline scenario.
        """
        # Diesel emissions
        baseline_diesel_co2 = baseline_diesel_l_per_day * cls.DIESEL_EF * 365 / 1000  # tons/year
        optimized_diesel_co2 = optimized_diesel_l_per_day * cls.DIESEL_EF * 365 / 1000
        
        # Grid emissions (if applicable)
        baseline_grid_co2 = baseline_grid_kwh_per_day * cls.GRID_EF * 365 / 1000
        optimized_grid_co2 = optimized_grid_kwh_per_day * cls.GRID_EF * 365 / 1000
        
        total_baseline = baseline_diesel_co2 + baseline_grid_co2
        total_optimized = optimized_diesel_co2 + optimized_grid_co2
        avoided = total_baseline - total_optimized
        
        return {
            "baseline_co2_tons_per_year": round(total_baseline, 2),
            "optimized_co2_tons_per_year": round(total_optimized, 2),
            "avoided_co2_tons_per_year": round(avoided, 2),
            "carbon_credit_revenue_usd": round(avoided * settings.CARBON_PRICE_USD_PER_TON, 2),
            "methodology": "AMS-I.D (Grid-connected renewable electricity generation)",
            "verification_required": True
        }
