import streamlit as st
import pandas as pd
import requests
import json
import time

# Configuration
API_URL = "http://localhost:8000"

st.set_page_config(page_title="Ingestion Dashboard", layout="wide")

st.title("📊 OAuth Ingestion Orchestrator")
st.markdown("Monitor and control your data ingestion pipelines.")

# Sidebar Controls
st.sidebar.header("⚙️ Pipeline Controls")
project_id = st.sidebar.text_input("Project ID", value="demo_project")

if st.sidebar.button("🚀 Run Ingestion Job"):
    with st.spinner(f"Ingesting data for {project_id}..."):
        try:
            # Simulate processing time for demo effect
            time.sleep(1.5)
            response = requests.post(f"{API_URL}/ingest", json={"project_id": project_id})
            if response.status_code == 200:
                result = response.json()
                st.sidebar.success(f"Success! {result['records_ingested']} records stored.")
            else:
                st.sidebar.error(f"Job Failed: {response.text}")
        except requests.exceptions.ConnectionError:
            st.sidebar.error("❌ Could not connect to Backend API. Is uvicorn running?")

# Main View
st.subheader("📈 Data Explorer")

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🔄 Refresh View"):
        st.rerun()

# Fetch Data
try:
    response = requests.get(f"{API_URL}/data", params={"project_id": project_id})
    if response.status_code == 200:
        payload = response.json()
        raw_data = payload.get("data", [])
        
        if raw_data:
            df = pd.DataFrame(raw_data)
            
            # KPI Cards
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Total Records", len(df))
            k2.metric("Total Spend", f"${df['spend'].sum():,.2f}")
            k3.metric("Impressions", f"{df['impressions'].sum():,}")
            k4.metric("Avg CTR", f"{(df['ctr'].mean() * 100):.2f}%")
            
            # Visualizations
            st.divider()
            c1, c2 = st.columns(2)
            
            with c1:
                st.markdown("#### Spend per Campaign")
                st.bar_chart(df, x="campaign_name", y="spend")
                
            with c2:
                st.markdown("#### Impressions vs Clicks")
                st.scatter_chart(df, x="impressions", y="clicks")
            
            # Raw Data Table
            st.divider()
            st.markdown("#### Processed Data Records")
            st.dataframe(df)
            
        else:
            st.info("No data found. Run an ingestion job to generate data.")
    else:
        st.warning("Could not fetch data.")
        
except requests.exceptions.ConnectionError:
    st.warning("⚠️ Backend API is not reachable. Please start the FastAPI server.")
