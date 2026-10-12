# Open synthetic warehouse usage dataset

`warehouse_usage.csv` contains **270 original fictional records**, three warehouses over 90 calendar days, and is dedicated to **CC0 1.0** (https://creativecommons.org/publicdomain/zero/1.0/). These are deliberately illustrative records, not observed cloud invoices, real clients, or vendor billing rates.

The original committed CSV was created deterministically for this project. `python -m warehouse.data` creates a separate reproducible randomly generated example with the same column schema but different numeric values; running it will overwrite the CSV. The ETL works with either.

Fields: `date`, `warehouse`, `compute_hours`, `usd_per_hour`, `queries`, `data_scanned_gb`, and `idle_ratio`.

Modeled cost = compute hours × fictional hourly rate. Savings estimates assume 50% of modeled idle cost can be recovered; this is a hypothesis, not a validated cost reduction. To evaluate actual savings, import authorized cloud billing exports and query-performance metrics, then confirm SLAs before changing anything.
