import os
import pandas as pd
import requests
import streamlit as st
st.set_page_config(page_title="Warehouse FinOps Control Center",layout="wide")
st.title("Data Warehouse Cost Optimization")
st.caption("Open CC0 synthetic usage · Bronze / Silver / Gold · Read-only AI recommendations")
api=os.getenv("API_URL","http://localhost:8000")
try:
    r=requests.get(api+"/api/costs",timeout=8);r.raise_for_status();result=r.json()
except requests.RequestException:
    result={"report":None,"warehouses":[]}
report=result.get("report")
if report:
    a,b,c=st.columns(3)
    a.metric("Modeled compute cost",f"${report['total_cost_usd']:,.2f}")
    b.metric("Heuristic saving opportunity",f"${report['potential_savings_usd']:,.2f}")
    c.metric("Rejected records",report["rejected"])
    st.info(report["note"])
    if st.button("Explain optimization opportunities"):
        try:
            response=requests.post(api+"/api/ai/recommend",timeout=100)
            response.raise_for_status();st.json(response.json())
        except requests.RequestException as exc:st.error(str(exc))
else:st.info("Run the ETL pipeline to generate cost analytics.")
if result.get("warehouses"):
    frame=pd.DataFrame(result["warehouses"])
    st.subheader("Cost by warehouse")
    st.bar_chart(frame.set_index("warehouse")["total_cost_usd"])
    st.dataframe(frame,use_container_width=True)
