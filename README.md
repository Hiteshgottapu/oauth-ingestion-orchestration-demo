# 🚀 OAuth Data Ingestion & Orchestration Demo

## 📖 Overview
This project demonstrates a robust, mock data ingestion pipeline designed for high scalability and secure operations. It simulates the extraction of advertising data (e.g., Google Ads, Facebook Ads) using **OAuth 2.0** authentication, processes it, and stores it in a simulated data lake (S3).

The purpose is to showcase **Software Architecture**, **OAuth Token Management**, and **Orchestration Logic** without dealing with real credentials or external API costs.

## 🏗 Architecture
1. **FastAPI Backend (`app/`)**: The core orchestration engine exposing REST endpoints.
2. **Mock OAuth Provider (`mock_oauth_provider.py`)**: Simulates the full OAuth lifecycle (Auth Code Grant, Token Expiry, Refresh Tokens).
3. **Ingestion Engine (`ingestion.py`)**: Fetches data using valid tokens, handling simulated network jitter and API failures.
4. **Data Lake Storage (`storage.py`)**: storing JSON files locally with timestamp-based partitioning (mock S3 behavior).
5. **Streamlit Dashboard (`dashboard/`)**: A user-friendly interface to trigger pipelines and visualize business metrics.

## 📦 Key Components

| Component | File | Description |
|-----------|------|-------------|
| **Entry Point** | `app/main.py` | FastAPI app with `/ingest` and `/health` routes. |
| **Auth** | `app/oauth.py` | Manages token retrieval and auto-refresh logic. |
| **Mock Provider** | `app/mock_oauth_provider.py` | Generates fake Access & Refresh tokens. |
| **Storage** | `app/storage.py` | Handles filesystem reads/writes (Mock S3). |
| **Pipeline** | `app/ingestion.py` | Connects Auth + API Fetch + Storage. |

## 🔐 Simulated OAuth Flow
1. **Check Token**: System checks in-memory store for a valid Access Token.
2. **Auth Code Flow**: If no token exists, it exchanges a "Code" for an Access/Refresh pair.
3. **Auto-Refresh**: If the Access Token is expired (simulated), it uses the Refresh Token to rotate credentials seamlessy before the API call.

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Backend API
Start the orchestration server:
```bash
uvicorn app.main:app --reload
```
*API will be available at [http://localhost:8000](http://localhost:8000)*

### 3. Run the Dashboard
In a new terminal, launch the UI:
```bash
streamlit run dashboard/dashboard_app.py
```

## 🧪 Testing the Flow
1. Open the Dashboard.
2. **Verify Project ID**: Ensure the default `demo_project` is selected or enter a custom one.
3. Click **🚀 Run Ingestion Job** to trigger a mock ingestion workflow.
4. Watch as the system authenticates, fetches mock data, and saves it.
5. Review the generated charts and tables.

## ⚠️ Disclaimer
**This is a SANITIZED DEMO.**
- No real real-world credentials are used.
- "Storage" is local execution.
- "OAuth" is logical simulation only.
- Designed for architectural review.
