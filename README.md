🚀 OAuth Data Ingestion & Orchestration Demo

📖 Overview
This repository contains a sanitized, runnable demo that showcases an OAuth 2.0–based
data ingestion and orchestration pipeline.

It simulates the extraction of advertising data (e.g., Google Ads, Facebook Ads),
processes it through a backend orchestration layer, and stores the output in a
locally simulated data lake (mock S3).

The goal is to demonstrate system architecture, OAuth token lifecycle management,
and orchestration patterns — without using real credentials or external APIs.

---

🏗 Architecture

• FastAPI Backend (app/)
  Acts as the orchestration layer and exposes REST endpoints to trigger ingestion
  and retrieve processed data.

• Mock OAuth Provider (mock_oauth_provider.py)
  Simulates the OAuth 2.0 Authorization Code flow, token expiration, and refresh logic.

• Ingestion Engine (ingestion.py)
  Uses valid tokens to fetch mock data, simulating network latency and API failures.

• Data Lake Storage (storage.py)
  Persists JSON files locally using timestamp-based partitioning to mimic S3 behavior.

• Streamlit Dashboard (dashboard/)
  Provides a lightweight control plane to trigger ingestion jobs and visualize outputs.

---

📦 Key Components

Component        File                     Description
---------------------------------------------------------------
Entry Point      app/main.py              FastAPI app with /ingest and /health routes
Auth             app/oauth.py             Token retrieval and auto-refresh logic
Mock Provider    app/mock_oauth_provider.py Generates fake access & refresh tokens
Storage          app/storage.py           Local filesystem read/write (mock S3)
Pipeline         app/ingestion.py         Connects Auth → Fetch → Storage

---

🔐 Simulated OAuth Flow

1. Token Check
   The system checks an in-memory store for a valid access token.

2. Authorization Code Flow
   If no valid token exists, a mock authorization code is exchanged for
   access and refresh tokens.

3. Auto-Refresh
   When the access token expires (simulated), the refresh token is used to
   rotate credentials before making the ingestion call.

---

🚀 Getting Started

1. Install Dependencies
   pip install -r requirements.txt

2. Run the Backend API
   uvicorn app.main:app --reload
   API available at: http://localhost:8000

3. Run the Dashboard
   streamlit run dashboard/dashboard_app.py

---

🧪 Testing the Flow

1. Open the Streamlit dashboard.
2. Verify the default project_id (demo_project) or enter a custom one.
3. Click “Run Ingestion Job” to trigger the pipeline.
4. The backend simulates OAuth authentication, ingests mock data, and persists it.
5. The dashboard refreshes to display aggregated metrics and processed records.

---

⚠️ Disclaimer

This is a SANITIZED DEMO.

• No real credentials or third-party APIs are used.
• Storage is local and simulates S3 behavior.
• OAuth is a logical simulation for architectural demonstration only.
• This project is intended for system design and orchestration review.
