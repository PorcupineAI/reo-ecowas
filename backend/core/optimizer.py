import numpy as np
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus
from typing import Dict, Tuple
from datetime import datetime, timedelta

class EnergyOptimizer:
    """
    Linear Programming optimizer for mini-grid dispatch.
    Minimizes cost while maintaining power balance and battery constraints.
    """
    
    def __init__(self, site_id: str, solar_forecast: list, load_forecast: list):
        """
        Args:
            solar_forecast: List of 96 values (15-min intervals, 24 hours)
            load_forecast: List of 96 values (15-min intervals, 24 hours)
        """
        self.site_id = site_id
        self.solar_forecast = solar_forecast
        self.load_forecast = load_forecast
        self.n_intervals = len(solar_forecast)  # Should be 96
        
        # Default parameters (can be overridden from DB)
        self.diesel_cost_per_l = 0.85  # USD
        self.battery_capacity_kwh = 100
        self.battery_max_charge_rate = 20  # kW
        self.battery_max_discharge_rate = 20  # kW
        self.battery_min_soc = 0.20
        self.battery_max_soc = 0.90
        self.diesel_max_kw = 30
        self.diesel_efficiency = 3.5  # kWh per liter
        
    def optimize(self) -> Dict:
        """
        Solve the dispatch optimization problem.
        Returns optimal dispatch schedule and metrics.
        """
        T = self.n_intervals
        dt = 0.25  # 15 minutes in hours
        
        # Create LP problem
        prob = LpProblem("MiniGridDispatch", LpMinimize)
        
        # Decision variables
        diesel = LpVariable.dicts("Diesel", range(T), lowBound=0, upBound=self.diesel_max_kw)
        battery_discharge = LpVariable.dicts("BattDischarge", range(T), lowBound=0, 
                                              upBound=self.battery_max_discharge_rate)
        battery_charge = LpVariable.dicts("BattCharge", range(T), lowBound=0,
                                           upBound=self.battery_max_charge_rate)
        grid_import = LpVariable.dicts("GridImport", range(T), lowBound=0, upBound=50)
        battery_soc = LpVariable.dicts("SOC", range(T+1), lowBound=self.battery_min_soc * self.battery_capacity_kwh,
                                        upBound=self.battery_max_soc * self.battery_capacity_kwh)
        
        # Objective: Minimize cost
        prob += lpSum([
            (diesel[t] / self.diesel_efficiency) * self.diesel_cost_per_l +  # Diesel cost
            0.02 * battery_discharge[t] * dt +  # Battery degradation cost
            0.15 * grid_import[t] * dt  # Grid import cost
            for t in range(T)
        ])
        
        # Initial SOC
        prob += battery_soc[0] == 0.50 * self.battery_capacity_kwh  # Start at 50%
        
        # Power balance and SOC dynamics
        for t in range(T):
            # Power balance: Solar + Discharge + Diesel + Grid = Load + Charge
            prob += (
                self.solar_forecast[t] + battery_discharge[t] + diesel[t] + grid_import[t]
                == self.load_forecast[t] + battery_charge[t]
            )
            
            # SOC update
            if t < T - 1:
                prob += battery_soc[t+1] == battery_soc[t] + (battery_charge[t] - battery_discharge[t]) * dt
        
        # Solve
        prob.solve()
        
        # Extract results
        if LpStatus[prob.status] == "Optimal":
            total_diesel_l = sum(diesel[t].varValue for t in range(T)) / self.diesel_efficiency
            total_diesel_cost = total_diesel_l * self.diesel_cost_per_l
            
            return {
                "status": "optimal",
                "total_diesel_liters": total_diesel_l,
                "total_diesel_cost_usd": total_diesel_cost,
                "total_grid_import_kwh": sum(grid_import[t].varValue for t in range(T)) * dt,
                "battery_cycles": sum(battery_discharge[t].varValue for t in range(T)) * dt / self.battery_capacity_kwh,
                "diesel_schedule": [diesel[t].varValue for t in range(T)]
            }
        else:
            return {"status": "infeasible", "error": "No feasible solution found"}
