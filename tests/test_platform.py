import pandas as pd
from fastapi.testclient import TestClient
from backend.main import app
from warehouse.data import generate
from warehouse.pipeline import run
from warehouse.ai import explain

def test_data():
    df=generate(4)
    assert len(df)==12
    assert df["idle_ratio"].between(0,1).all()

def test_pipeline(tmp_path):
    csv=tmp_path/"sample.csv";generate(4).to_csv(csv,index=False)
    report=run(str(csv),str(tmp_path/"data"),str(tmp_path/"reports"))
    assert report["raw"]==12 and report["valid"]==12
    assert report["total_cost_usd"]>0
    assert report["potential_savings_usd"]>0

def test_api(monkeypatch,tmp_path):
    monkeypatch.setenv("REPORT_PATH",str(tmp_path/"missing.json"))
    monkeypatch.setenv("GOLD_PATH",str(tmp_path/"missing.parquet"))
    c=TestClient(app)
    assert c.get("/health").status_code==200
    assert c.get("/api/costs").json()["warehouses"]==[]
    assert c.post("/api/ai/recommend").status_code==404

def test_mock(monkeypatch):
    monkeypatch.setenv("LLM_MODE","mock")
    assert explain({"raw":1,"valid":1,"rejected":0,"total_cost_usd":10,"potential_savings_usd":2,"note":"demo"})["approval_required"]
