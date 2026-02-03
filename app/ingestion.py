import random
import logging
from typing import List, Dict, Any
from app.oauth import get_oauth_token
from app.storage import write_raw_data

logger = logging.getLogger(__name__)

def fetch_mock_ads_data(access_token: str) -> List[Dict[str, Any]]:
    """
    Simulates an HTTP GET to an external Ads API.
    """
    # Simulate Auth Check
    if not access_token:
        raise ValueError("No access token provided")
        
    # Simulate random API failure (Networking, 500s)
    if random.random() < 0.15:
        raise ConnectionError("External API Gatekeeper Timeout")

    # Generate Mock Data
    campaigns = ["Summer Promo", "Winter clearance", "Brand Awareness", "Retargeting Q3", "Competitor Conquest"]
    data = []
    
    count = random.randint(10, 50)
    for i in range(count):
        data.append({
            "id": f"ad_{random.randint(10000, 99999)}",
            "campaign_name": random.choice(campaigns),
            "impressions": random.randint(500, 10000),
            "clicks": random.randint(10, 500),
            "spend": round(random.uniform(10.0, 300.0), 2),
            "date": "2023-11-01" 
        })
        
    return data

def run_ingestion_task(project_id: str = "demo_project") -> Dict[str, Any]:
    """
    Main entry point for the ingestion job.
    1. Authenticate (OAuth)
    2. Extract (Fetch)
    3. Load (Storage)
    """
    logger.info(f"Starting ingestion for project: {project_id}")
    
    try:
        # 1. Auth Phase
        token_envelope = get_oauth_token()
        access_token = token_envelope.get("access_token")
        
        # 2. Extraction Phase
        logger.info("Fetching data from External Ads API...")
        raw_data = fetch_mock_ads_data(access_token)
        logger.info(f"Successfully fetched {len(raw_data)} records.")
        
        # 3. Load Phase
        metadata = {
            "source": "MockAdsAPI",
            "project_id": project_id,
            "job_status": "success"
        }
        saved_path = write_raw_data(raw_data, metadata)
        
        return {
            "status": "success",
            "message": "Ingestion completed successfully",
            "records_ingested": len(raw_data),
            "storage_path": saved_path
        }
        
    except Exception as e:
        logger.error(f"Ingestion job failed: {e}")
        return {
            "status": "failed",
            "message": str(e),
            "records_ingested": 0
        }
