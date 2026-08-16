#!/usr/bin/env python3
"""
Seed gender metrics and policy compliance data for REO-ECOWAS.
Uses the same database connection as the main application.
Requires sites to already exist (run load_geodata.py first).
"""

import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend.models import Site, GenderMetrics, GenderPolicyCompliance
from backend.core.gender import GenderInclusionEngine


def seed_gender_metrics():
    """
    Generate random but realistic gender metrics for each existing site.
    """
    db = SessionLocal()
    try:
        # Clear existing gender metrics (optional)
        db.query(GenderMetrics).delete()

        sites = db.query(Site).all()
        if not sites:
            print("❌ No sites found. Please run load_geodata.py first.")
            return

        for site in sites:
            # Generate realistic values (West Africa averages + randomness)
            gender_data = {
                "female_headed_households": random.randint(20, 150),
                "female_energy_entrepreneurs": random.randint(2, 25),
                "female_employees_percent": round(random.uniform(15, 45), 1),
                "female_decision_makers_percent": round(random.uniform(10, 50), 1),
                "women_using_clean_cooking": random.randint(50, 300),
                "girls_school_attendance_impact": round(random.uniform(0.05, 0.35), 2),
                "women_income_generation": round(random.uniform(500, 15000), 0),
                "gender_consultations_completed": random.choice([True, False]),
                "gender_action_plan_exists": random.choice([True, False]),
                "safety_measures_for_women": random.choice([True, False]),
                "women_targeted_beneficiary": random.choice([True, False]),
            }

            # Compute derived scores
            gender_data["gender_inclusion_score"] = (
                GenderInclusionEngine.compute_gender_inclusion_score(gender_data)
            )
            gender_data["gender_equality_index"] = round(random.uniform(0.4, 0.9), 3)
            gender_data["sdg5_alignment_score"] = round(random.uniform(40, 90), 1)
            gender_data["data_quality_score"] = round(random.uniform(60, 95), 1)

            metrics = GenderMetrics(
                site_id=site.id,
                **gender_data
            )
            db.add(metrics)

        db.commit()
        print(f"✅ Seeded gender metrics for {len(sites)} sites.")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


def seed_gender_policy():
    """
    Seed gender policy compliance scores for ECOWAS countries.
    Based on realistic assessments from World Bank/UNDP reports.
    """
    db = SessionLocal()
    try:
        db.query(GenderPolicyCompliance).delete()

        # Realistic scores (1–5) for 15 ECOWAS countries
        policy_data = {
            "Nigeria": {"assessment": 3, "budgeting": 2, "leadership": 3, "data": 3, "consultation": 2},
            "Benin": {"assessment": 4, "budgeting": 3, "leadership": 3, "data": 4, "consultation": 4},
            "Togo": {"assessment": 3, "budgeting": 2, "leadership": 2, "data": 3, "consultation": 3},
            "Ghana": {"assessment": 4, "budgeting": 4, "leadership": 4, "data": 4, "consultation": 4},
            "Côte d'Ivoire": {"assessment": 3, "budgeting": 3, "leadership": 3, "data": 3, "consultation": 3},
            "Senegal": {"assessment": 4, "budgeting": 3, "leadership": 4, "data": 4, "consultation": 3},
            "Mali": {"assessment": 2, "budgeting": 2, "leadership": 2, "data": 2, "consultation": 2},
            "Burkina Faso": {"assessment": 3, "budgeting": 3, "leadership": 3, "data": 3, "consultation": 3},
            "Niger": {"assessment": 2, "budgeting": 2, "leadership": 2, "data": 2, "consultation": 2},
            "Guinea": {"assessment": 2, "budgeting": 2, "leadership": 2, "data": 2, "consultation": 2},
            "Liberia": {"assessment": 3, "budgeting": 3, "leadership": 3, "data": 3, "consultation": 3},
            "Sierra Leone": {"assessment": 3, "budgeting": 3, "leadership": 3, "data": 3, "consultation": 3},
            "The Gambia": {"assessment": 4, "budgeting": 3, "leadership": 3, "data": 3, "consultation": 4},
            "Cabo Verde": {"assessment": 5, "budgeting": 4, "leadership": 4, "data": 4, "consultation": 4},
            "Guinea-Bissau": {"assessment": 2, "budgeting": 2, "leadership": 2, "data": 2, "consultation": 2},
        }

        for country, scores in policy_data.items():
            policy = GenderPolicyCompliance(
                country=country,
                gender_assessment_mandate=scores["assessment"],
                gender_budgeting=scores["budgeting"],
                women_in_energy_ministry=scores["leadership"],
                gender_data_collection=scores["data"],
                community_consultation=scores["consultation"],
            )
            # Compute policy alignment score (average of the five, converted to %)
            avg = (
                scores["assessment"] +
                scores["budgeting"] +
                scores["leadership"] +
                scores["data"] +
                scores["consultation"]
            ) / 5
            policy.policy_alignment_score = round((avg / 5) * 100, 1)
            db.add(policy)

        db.commit()
        print(f"✅ Seeded gender policy data for {len(policy_data)} countries.")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🌿 Seeding gender data...")
    seed_gender_metrics()
    seed_gender_policy()
    print("✅ Gender data seeding complete.")
