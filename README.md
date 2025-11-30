# College Football PPG Visualizer API

Containerized Flask API that serves graphs comparing **Points Per Game (PPG)** to four other
key college football statistics. Includes Docker support and an optional cloud deployment.

---

## 1) Executive Summary

**Problem.**  
College football fans and analysts often look at points per game, but it’s not always obvious
how scoring relates to other on-field metrics (passing TDs, rushing yards, turnovers, etc.).
There’s also friction in spinning up quick, reproducible visual analyses.

**Solution.**  
This project provides a lightweight web API that exposes multiple endpoints, each returning
a visualization of **PPG vs another statistic** from a college football dataset. The service
is packaged in a Docker container for reproducible runs and optionally deployed to the cloud
for easy sharing.

---

## 2) System Overview

**Course Concept(s).**  
- Flask REST API with multiple endpoints  
- Data loading / simple pipeline from CSV into Pandas  
- Containerization via Docker (deterministic build and one-command run)

**Architecture Diagram.**  
See `assets/architecture.png`.

High-level flow:

Client → Flask API → Data Loader (Pandas) → Plotting Module (Matplotlib/Plotly) → PNG/HTML Response

**Data / Models / Services.**

- **Dataset:** College football team statistics  
- **Format:** CSV (e.g., one row per team-season)  
- **Example fields:** `team`, `season`, `points_per_game`, `pass_td_per_game`,
  `rush_yds_per_game`, `total_yds_per_game`, `turnovers_per_game`  
- **Size:** Small enough to load in memory (a few MB)  
- **License:** _[Fill in data source + license]_  

No ML models are used; the API focuses on descriptive visualization.

---

## 3) How to Run (Local with Docker)

### Prerequisites

- Docker installed
- (Optional) `make` if you prefer `make run`

### Environment Variables

Copy `.env.example` to `.env` and adjust as needed:

```bash
cp .env.example .env
