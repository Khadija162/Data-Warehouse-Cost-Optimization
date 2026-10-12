"""Bronze/Silver/Gold warehouse usage ETL with deterministic cost metrics."""
import argparse
import json
from pathlib import Path
import pandas as pd

FIELDS=["date","warehouse","compute_hours","usd_per_hour","queries","data_scanned_gb","idle_ratio"]

def run(source="data/public/warehouse_usage.csv",output="data",reports="artifacts"):
    frame=pd.read_csv(source)
    missing=set(FIELDS)-set(frame.columns)
    if missing:raise ValueError(f"Missing columns: {sorted(missing)}")
    root=Path(output)
    for layer in ("bronze","silver","gold"):(root/layer).mkdir(parents=True,exist_ok=True)
    frame.to_parquet(root/"bronze"/"usage.parquet",index=False)
    numeric=frame[FIELDS[2:]].apply(pd.to_numeric,errors="coerce")
    valid=numeric.notna().all(axis=1)&numeric.ge(0).all(axis=1)
    valid &= numeric["idle_ratio"].le(1)&pd.to_datetime(frame["date"],errors="coerce").notna()
    valid &=frame["warehouse"].notna()&frame["warehouse"].astype(str).str.len().gt(0)
    clean=frame.loc[valid].copy()
    clean["estimated_compute_cost_usd"]=numeric.loc[valid,"compute_hours"]*numeric.loc[valid,"usd_per_hour"]
    clean["estimated_idle_cost_usd"]=clean["estimated_compute_cost_usd"]*numeric.loc[valid,"idle_ratio"]
    clean.to_parquet(root/"silver"/"usage.parquet",index=False)
    frame.loc[~valid].to_parquet(root/"silver"/"rejected.parquet",index=False)
    gold=clean.groupby("warehouse",as_index=False).agg(
        usage_days=("date","nunique"),compute_hours=("compute_hours","sum"),queries=("queries","sum"),
        total_cost_usd=("estimated_compute_cost_usd","sum"),idle_cost_usd=("estimated_idle_cost_usd","sum"),
        data_scanned_gb=("data_scanned_gb","sum"))
    gold["estimated_savings_usd"]=gold["idle_cost_usd"]*.5
    gold.to_parquet(root/"gold"/"warehouse_costs.parquet",index=False)
    report={"raw":int(len(frame)),"valid":int(len(clean)),"rejected":int((~valid).sum()),
       "total_cost_usd":round(float(gold["total_cost_usd"].sum()),2),
       "potential_savings_usd":round(float(gold["estimated_savings_usd"].sum()),2),
       "note":"Illustrative cost = hours x rate. Estimated savings assume recovering 50% of idle cost, not guaranteed."}
    path=Path(reports)/"latest.json";path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,indent=2),encoding="utf-8")
    return report

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--source",default="data/public/warehouse_usage.csv")
    a=p.parse_args();print(json.dumps(run(a.source),indent=2))
