class GenderInclusionEngine:
    @classmethod
    def compute_gender_inclusion_score(cls, data):
        score = 0
        score += data.get("female_headed_households", 0) * 0.01
        score += data.get("female_energy_entrepreneurs", 0) * 0.02
        score += data.get("female_employees_percent", 0) * 0.5
        return min(100, score)
