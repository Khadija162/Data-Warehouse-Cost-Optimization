"""Deterministic original CC0 synthetic warehouse usage data."""
from pathlib import Path
import numpy as np
import pandas as pd

def generate(days=90, seed=42):
    rng=np.random.default_rng(seed)
    rows=[]
    for day in pd.date_range("2025-01-01",periods=days):
        for name, rate in [("analytics",2.5),("finance",3.4),("experiments",1.7)]:
            duration=round(float(rng.uniform(1,18)),2)
            queries=int(rng.integers(5,320))
            scanned=round(float(rng.uniform(2,900)),2)
            idle=round(float(rng.uniform(0,.75)),3)
            rows.append({"date":day.date().isoformat(),"warehouse":name,"compute_hours":duration,"usd_per_hour":rate,
              "queries":queries,"data_scanned_gb":scanned,"idle_ratio":idle})
    return pd.DataFrame(rows)

if __name__=="__main__":
    path=Path("data/public/warehouse_usage.csv");path.parent.mkdir(parents=True,exist_ok=True)
    generate().to_csv(path,index=False);print(path)
