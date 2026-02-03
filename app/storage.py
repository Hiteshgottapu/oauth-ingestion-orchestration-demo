import json
import os
import glob
from datetime import datetime
from typing import Dict, List, Any
from app.config import settings

def ensure_storage_path():
    """Ensures the local storage simulation directory exists."""
    if not os.path.exists(settings.STORAGE_PATH):
        os.makedirs(settings.STORAGE_PATH)

def write_raw_data(data: List[Dict[str, Any]], metadata: Dict[str, Any]) -> str:
    """
    Writes raw data to the file system, partitioned by project and date.
    Returns the file path written.
    """
    ensure_storage_path()
    
    project_id = metadata.get("project_id", "default_project")
    ingestion_date = datetime.now().strftime("%Y-%m-%d")
    
    # Partition structure: storage/project_id/YYYY-MM-DD/
    partition_path = os.path.join(settings.STORAGE_PATH, project_id, ingestion_date)
    os.makedirs(partition_path, exist_ok=True)
    
    timestamp = int(datetime.now().timestamp())
    filename = f"raw_ingest_{timestamp}.json"
    file_path = os.path.join(partition_path, filename)
    
    output_content = {
        "metadata": metadata,
        "record_count": len(data),
        "data": data,
        "ingested_at_iso": datetime.now().isoformat()
    }
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(output_content, f, indent=2)
        
    return file_path

def read_stored_data(project_id: str, date_filter: str = None) -> List[Dict[str, Any]]:
    """
    Reads data back from storage.
    If date_filter (YYYY-MM-DD) is provided, only reads that partition.
    Otherwise reads all data for the project.
    """
    if not os.path.exists(settings.STORAGE_PATH):
        return []
        
    base_path = os.path.join(settings.STORAGE_PATH, project_id)
    search_pattern = os.path.join(base_path, "*", "*.json")
    
    if date_filter:
        search_pattern = os.path.join(base_path, date_filter, "*.json")
        
    files = glob.glob(search_pattern)
    all_data = []
    
    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                content = json.load(f)
                # We extract the 'data' list from the container
                if "data" in content and isinstance(content["data"], list):
                    all_data.extend(content["data"])
        except Exception as e:
            print(f"Error reading file {file}: {e}")
            
    return all_data
