from datetime import datetime, timezone
from typing import List, Dict, Any

def preprocess_data(raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Cleans and normalizes the ingested data.
    - Validates schema
    - Removes invalid records
    - Normalizes types
    - Adds timestamps
    """
    processed = []
    
    for record in raw_data:
        # 1. Schema Validation (Simulated)
        if "id" not in record or "campaign_name" not in record:
            continue # Skip invalid records
            
        clean_record = record.copy()
        
        # 2. String Normalization
        clean_record["campaign_name"] = str(clean_record["campaign_name"]).strip().title()
        
        # 3. Metric Type Casting
        try:
            clean_record["impressions"] = int(record.get("impressions", 0))
            clean_record["clicks"] = int(record.get("clicks", 0))
            clean_record["spend"] = float(record.get("spend", 0.0))
        except (ValueError, TypeError):
            # Fallback to 0 if data is corrupt
            clean_record["impressions"] = 0
            clean_record["clicks"] = 0
            clean_record["spend"] = 0.0
            
        # 4. Computed Fields (e.g. CTR, CPC)
        imps = clean_record["impressions"]
        clicks = clean_record["clicks"]
        spend = clean_record["spend"]
        
        clean_record["ctr"] = (clicks / imps) if imps > 0 else 0.0
        clean_record["cpc"] = (spend / clicks) if clicks > 0 else 0.0
        
        # 5. Metadata
        # Use timezone-aware UTC datetime
        clean_record["processed_at"] = datetime.now(timezone.utc).isoformat()
        
        processed.append(clean_record)
        
    return processed
