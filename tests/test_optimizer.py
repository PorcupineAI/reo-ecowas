
### `tests/test_optimizer.py` — Unit Tests

```python
import pytest
import numpy as np
from backend.core.optimizer import EnergyOptimizer
from backend.core.carbon import CarbonFinanceCalculator

class TestEnergyOptimizer:
    """Test the linear programming dispatch optimizer."""

    def test_optimizer_runs_optimally(self):
        """Test that the optimizer returns an optimal solution for valid inputs."""
        solar = np.linspace(0, 15, 96).tolist()  # Simple ramp
        load = [10] * 96  # Constant load
        
        optimizer = EnergyOptimizer(
            site_id="test-site",
            solar_forecast=solar,
            load_forecast=load
        )
        result = optimizer.optimize()
        
        assert result["status"] == "optimal"
        assert "total_diesel_liters" in result
        assert "total_diesel_cost_usd" in result
        assert isinstance(result["total_diesel_liters"], float)

    def test_optimizer_handles_high_load(self):
        """Test optimizer behavior when load exceeds available generation."""
        solar = [0] * 96  # No solar
        load = [50] * 96  # Very high load
        
        optimizer = EnergyOptimizer(
            site_id="test-site",
            solar_forecast=solar,
            load_forecast=load
        )
        result = optimizer.optimize()
        
        # Should still be feasible (uses diesel + grid)
        assert result["status"] == "optimal"
        assert result["total_diesel_liters"] > 0

class TestCarbonFinanceCalculator:
    """Test carbon finance calculations."""

    def test_co2_reduction_calculation(self):
        """Test basic CO2 avoided calculation."""
        result = CarbonFinanceCalculator.calculate_avoided_emissions(
            baseline_diesel_l_per_day=50,
            optimized_diesel_l_per_day=18
        )
        
        # 50 - 18 = 32 L/day saved
        # 32 * 2.68 kg/L * 365 / 1000 = 31.3 tons/year
        expected_co2 = 32 * 2.68 * 365 / 1000
        assert abs(result["avoided_co2_tons_per_year"] - expected_co2) < 0.01
        assert result["carbon_credit_revenue_usd"] > 0
        assert result["methodology"] == "AMS-I.D"

    def test_zero_savings(self):
        """Test edge case: no diesel savings."""
        result = CarbonFinanceCalculator.calculate_avoided_emissions(
            baseline_diesel_l_per_day=50,
            optimized_diesel_l_per_day=50
        )
        assert result["avoided_co2_tons_per_year"] == 0
        assert result["carbon_credit_revenue_usd"] == 0
