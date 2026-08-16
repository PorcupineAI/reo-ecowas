class CarbonFinanceCalculator:
    DIESEL_EF = 2.68

    @classmethod
    def calculate_avoided_emissions(cls, baseline_diesel_l_per_day, optimized_diesel_l_per_day, **kwargs):
        avoided = baseline_diesel_l_per_day - optimized_diesel_l_per_day
        co2 = avoided * cls.DIESEL_EF * 365 / 1000
        return {
            "avoided_co2_tons_per_year": round(co2, 2),
            "carbon_credit_revenue_usd": round(co2 * 35, 2)
    }
