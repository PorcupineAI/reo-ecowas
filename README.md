# ⚡ REO-ECOWAS: Regional Energy Orchestration Platform

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-teal.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)](https://streamlit.io/)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/yourusername/reo-ecowas)

**A policy decision-support tool for ECOWAS energy transition planning.**

REO-ECOWAS helps Programme Officers and energy planners visualize investment hotspots, benchmark regulatory environments, and estimate carbon finance potential—all without needing engineering expertise.

---

## 🎯 Why This Exists

- **35% transmission losses** across West Africa's grid
- **48% renewable target** by 2030 (ECOWAS Renewable Energy Policy)
- **$200M+** in climate finance flows awaiting bankable projects

This platform turns free satellite data + public policy indicators into actionable investment intelligence.

---

## ✨ Features

| Module | What it does |
|--------|--------------|
| **Geospatial Suitability** | Overlays solar, grid, population, and economic data to rank sites (0-100) |
| **Dispatch Optimizer** | Linear programming model minimizing diesel consumption with solar + storage |
| **Regulatory Matrix** | Scores 15 ECOWAS countries on tariff, import duty, land, and grid policy |
| **Carbon Finance MRV** | Estimates CO₂ avoided and potential carbon credit revenue (Gold Standard aligned) |
| **Policy Simulator** | Adjust regulatory scores in real-time to see impact on project feasibility |

---

## 🚀 Quick Start (30 seconds)

### Option A: One-click deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/yourusername/reo-ecowas)

### Option B: Local development

```bash
# Clone
git clone https://github.com/yourusername/reo-ecowas.git
cd reo-ecowas

# Start PostgreSQL with PostGIS
docker-compose up -d postgres

# Install Python deps
pip install -r requirements.txt

# Seed database
python scripts/init_db.py
python scripts/load_geodata.py

# Run backend
uvicorn backend.main:app --reload

# Run frontend (new terminal)
streamlit run frontend/app.py
