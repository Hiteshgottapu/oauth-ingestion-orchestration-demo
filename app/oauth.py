import logging
import time
from typing import Dict, Optional
from app.config import settings
from app.mock_oauth_provider import simulate_auth_code_flow, simulate_refresh_token_grant

logger = logging.getLogger(__name__)

# In-memory token store (mimicking a database or Redis cache)
_TOKEN_STORE: Dict[str, Dict] = {}

def get_oauth_token() -> Dict:
    """
    Retrieves a valid OAuth token.
    - Checks if a token exists in memory.
    - If missing, performs initial 'Auth Code' flow.
    - If present but expired, performs 'Refresh Token' flow.
    """
    global _TOKEN_STORE
    
    token_key = "current_session_token"
    token_data = _TOKEN_STORE.get(token_key)
    
    # 1. Initial Login / No Token
    if not token_data:
        logger.info("No active token found. Initiating full OAuth flow...")
        token_data = simulate_auth_code_flow(
            settings.MOCK_OAUTH_CLIENT_ID, 
            settings.MOCK_OAUTH_CLIENT_SECRET
        )
        _TOKEN_STORE[token_key] = token_data
        return token_data

    # 2. Check Expiration
    created_at = token_data.get("created_at", 0)
    expires_in = token_data.get("expires_in", 3600)
    expiry_time = created_at + expires_in
    
    # Refresh if expired or expiring in the next 60 seconds
    if time.time() > (expiry_time - 60):
        logger.info("Access token expired or expiring soon. Refreshing...")
        try:
            refresh_token = token_data.get("refresh_token")
            new_token_data = simulate_refresh_token_grant(refresh_token)
            
            # Update store
            _TOKEN_STORE[token_key] = new_token_data
            return new_token_data
        except Exception as e:
            logger.error(f"Token refresh failed: {e}. Re-authenticating.")
            # If refresh fails, fall back to fresh auth
            token_data = simulate_auth_code_flow(
                settings.MOCK_OAUTH_CLIENT_ID, 
                settings.MOCK_OAUTH_CLIENT_SECRET
            )
            _TOKEN_STORE[token_key] = token_data
            return token_data
            
    # 3. Token is valid
    return token_data
