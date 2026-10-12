# Data Warehouse Cost Optimization — Full-Stack FinOps Analytics

A **local warehouse FinOps engineering prototype** combining an openly reusable example dataset, Bronze/Silver/Gold Parquet processing, cost and idle-capacity analysis, a FastAPI backend, a Streamlit frontend, Docker, tests, optional open-weight AI explanations, and an Azure cloud blueprint.

> **Maturity:** Source files and sample data are in this repository. Cloud deployment and end-to-end container execution have not been verified. Estimated savings are a heuristic, not real billing reductions.

## Architecture

```text
CC0 synthetic warehouse usage (included)
    |
    +--> Pandas validation --> Bronze raw Parquet
                          --> Silver clean/rejected Parquet
                          --> Gold per-warehouse spend and idle costs
                                       |
                                  JSON report
                                       |
                                   FastAPI
                           /api/costs  /api/ai/recommend
                                       |
                               Streamlit dashboard
                         mock AI or local Ollama (optional)

CI: GitHub Actions + pytest + Docker build
Azure blueprint: ADLS Gen2 -> Databricks/Delta -> Container Apps -> Azure Monitor
```

## Open-source example data

Included: [data/public/warehouse_usage.csv](data/public/warehouse_usage.csv), **270 original synthetic records** across three warehouses over 90 days. Dedicated to **CC0 1.0**, so you can reuse it freely. It does **not** represent actual charges or a particular cloud vendor. Dataset facts and cost assumptions are recorded in [data provenance](data/public/README.md).

`python -m warehouse.data` optionally regenerates a new seeded sample dataset (the generated values may differ from the committed CSV).

## Windows PowerShell quick start

```powershell
git clone https://github.com/Khadija162/Data-Warehouse-Cost-Optimization.git
cd Data-Warehouse-Cost-Optimization
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m warehouse.pipeline
.\.venv\Scripts\python.exe -m pytest -q
```

The pipeline creates `data/bronze/`, `data/silver/`, `data/gold/warehouse_costs.parquet` and `artifacts/latest.json`.

### Backend and frontend

Start in separate terminals:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
.\.venv\Scripts\python.exe -m streamlit run frontend/app.py
```

API documentation: http://localhost:8000/docs
Dashboard: http://localhost:8501

Or, **after running the ETL once**, use Docker Desktop:

```powershell
docker compose up --build
```

The API mounts Gold analytics and reports as read-only Docker volumes. The dashboard fetches cost figures from FastAPI; it does not have direct data lake permissions.

## AI cost investigator

Default `LLM_MODE=mock` produces a deterministic explanation without credentials. For actual open-weight inference, install [Ollama](https://ollama.com/), download a supported model, and start **the host-side** backend:

```powershell
ollama pull qwen2.5:3b
$env:LLM_MODE="ollama"
$env:OLLAMA_MODEL="qwen2.5:3b"
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

Docker Compose defaults to mock mode. AI is read-only: it cannot pause, resize, delete or otherwise alter warehouses. Human approval and performance testing are mandatory before applying recommendations.

## Metrics and assumptions

- Estimated compute expense = `compute_hours × usd_per_hour`.
- Estimated idle expense = `compute expense × idle_ratio`.
- Hypothetical recoverable savings = **50% of modeled idle expense**, with no guarantee these savings could actually be realized.
- Invalid or missing metric values go into rejected Silver rows.

This is **cost analytics and heuristic optimization**, not trained machine-learning forecasting, billing-grade cost reconciliation, or an autonomous warehouse optimizer.

## Azure cloud roadmap

Azure Cost Management exports or approved vendor billing tables -> Azure Data Lake Storage Gen2 -> Azure Databricks/Delta Bronze/Silver/Gold -> API and dashboard hosted in Azure Container Apps -> Azure Monitor, Key Vault and managed identity. Optional model inference is via a separately hosted open-weight model. Terraform currently provisions **only an Azure resource group and ADLS storage** when manually applied. No Azure resources have been created by this update.

Public deployment requires authentication, authorization, secret management, networking isolation, budgets and audit logs. See [architecture](docs/architecture.md).

## Validation status

The files are committed. Tests, Docker startup, CI workflow results and Azure deployment have not been independently confirmed yet. Run `python -m pytest -q` and inspect GitHub Actions before treating the platform as verified.
