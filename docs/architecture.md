# Warehouse FinOps architecture

Current local implementation: original CC0 synthetic usage data -> Python/Pandas ETL -> Bronze/Silver/Gold Parquet -> model-derived per-warehouse estimated spend and idle-cost reduction -> JSON report -> FastAPI -> Streamlit. A mock analyst or opt-in open-weight Ollama model generates *read-only* investigative suggestions. Docker Compose and CI included.

Not yet implemented: real Azure/Snowflake/Databricks billing ingestion, production cost allocation, genuine predictive ML cost forecasts, autonomous resizing, historical drift detection, production access control, Spark/Delta or deployed Azure resources.

Cloud plan: collect supported Azure Cost Management exports and Databricks billing system tables -> ADLS Gen2 Bronze -> Spark Delta Silver/Gold -> operational metrics PostgreSQL -> FastAPI/Streamlit Azure Container Apps -> open-weight model inference on isolated GPU or Foundry supported deployment -> Azure Monitor and Key Vault. No resources are created automatically. Forecast quality and potential savings need real invoices, workload telemetry and SLA validation.
