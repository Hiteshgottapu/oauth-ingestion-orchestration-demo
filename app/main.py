import logging
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.config import settings
from app.ingestion import run_ingestion_task
from app.storage import read_stored_data
from app.preprocessing import preprocess_data

# Configure Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=settings.LOG_LEVEL
)
logger = logging.getLogger("main")

# Initialize App
app = FastAPI(title=settings.APP_NAME, description="Demo OAuth Ingestion System")

# Models
class IngestionRequest(BaseModel):
    project_id: str = "demo_project"

class IngestionResponse(BaseModel):
    status: str
    message: str
    records_ingested: int
    storage_path: Optional[str] = None

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.APP_NAME}"}

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "environment": settings.ENV}

@app.post("/ingest", response_model=IngestionResponse)
def trigger_ingestion(payload: IngestionRequest):
    """
    Manually triggers the ingestion pipeline for a specific project.
    """
    logger.info(f"Received ingestion request for {payload.project_id}")
    result = run_ingestion_task(payload.project_id)
    
    if result["status"] == "failed":
        logger.error(f"Ingestion failed: {result['message']}")
        raise HTTPException(status_code=500, detail=result["message"])
        
    return result

@app.get("/data", response_model=Dict[str, Any])
def fetch_processed_data(
    project_id: str = Query(..., description="Project ID to fetch data for"), 
    preprocess: bool = Query(True, description="Whether to clean/normalize data")
):
    """
    Fetches stored data for a project. 
    Can optionally skip preprocessing to return raw data.
    """
    raw_data = read_stored_data(project_id)
    
    if not raw_data:
        return {
            "project_id": project_id,
            "count": 0,
            "data": []
        }
    
    if preprocess:
        data_to_return = preprocess_data(raw_data)
    else:
        data_to_return = raw_data
        
    return {
        "project_id": project_id,
        "count": len(data_to_return),
        "data": data_to_return
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
