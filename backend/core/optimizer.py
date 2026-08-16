import numpy as np
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus

class EnergyOptimizer:
    def __init__(self, site_id: str, solar_forecast: list, load_forecast: list):
        self.site_id = site_id
        self.solar = solar_forecast
        self.load = load_forecast
        self.n = len(solar_forecast)

    def optimize(self):
        T = self.n
        prob = LpProblem("Dispatch", LpMinimize)
        diesel = LpVariable.dicts("D", range(T), 0, 50)
        discharge = LpVariable.dicts("Dis", range(T), 0, 20)
        charge = LpVariable.dicts("Ch", range(T), 0, 20)
        grid = LpVariable.dicts("G", range(T), 0, 50)
        soc = LpVariable.dicts("SOC", range(T+1), 20, 90)

        prob += lpSum(diesel[t] for t in range(T))
        prob += soc[0] == 50
        for t in range(T):
            prob += self.solar[t] + discharge[t] + diesel[t] + grid[t] == self.load[t] + charge[t]
            if t < T-1:
                prob += soc[t+1] == soc[t] + (charge[t] - discharge[t]) * 0.25

        prob.solve()
        if LpStatus[prob.status] != "Optimal":
            return {"status": "infeasible"}
        return {
            "status": "optimal",
            "total_diesel_liters": sum(diesel[t].varValue for t in range(T)),
            "total_diesel_cost_usd": sum(diesel[t].varValue for t in range(T)) * 0.85
        }
