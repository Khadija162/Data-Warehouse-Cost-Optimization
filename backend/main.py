"""Local read-only warehouse cost API."""
import json
import os
from pathlib import Path
import pandas as pd
import requests
from fastapi import FastAPI,HTTPException
from warehouse.ai import explain
app=FastAPI(title="Warehouse Cost Optimization",version="0.1.0")
def report():
    p=Path(os.getenv("REPORT_PATH","artifacts/latest.json"))
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None
@app.get("/health")
def health():return {"status":"ok","report_ready":report() is not None}
@app.get("/api/costs")
def costs():
    path=Path(os.getenv("GOLD_PATH","data/gold/warehouse_costs.parquet"))
    return {"report":report(),"warehouses":pd.read_parquet(path).round(2).to_dict(orient="records") if path.is_file() else []}
@app.post("/api/ai/recommend")
def recommend():
    r=report()
    if r is None:raise HTTPException(404,"Run ETL before requesting recommendations")
    try:return explain(r)
    except (requests.RequestException,ValueError,KeyError) as exc:raise HTTPException(502,"AI unavailable") from exc
