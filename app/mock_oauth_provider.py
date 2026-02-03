import time
import uuid
from typing import Dict, Any

# Mock backend storage for valid tokens
MOCK_TOKENS = {}

def simulate_auth_code_flow(client_id: str, client_secret: str) -> Dict[str, Any]:
    """
    Simulates exchanging credentials for an access token.
    In a real app, this would be an HTTP call to https://provider.com/oauth/token.
    """
    # Simulate validation
    if not client_id or not client_secret:
        raise ValueError("Missing client credentials")

    access_token = f"mock_at_{uuid.uuid4().hex[:8]}"
    refresh_token = f"mock_rt_{uuid.uuid4().hex[:8]}"
    expires_in = 3600  # 1 hour

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "expires_in": expires_in,
        "scope": "read write",
        "created_at": time.time()
    }

def simulate_refresh_token_grant(refresh_token: str) -> Dict[str, Any]:
    """
    Simulates exchanging a refresh token for a new access token.
    """
    # Simulate validation
    if not refresh_token.startswith("mock_rt_"):
        raise ValueError("Invalid refresh token")

    new_access_token = f"mock_at_{uuid.uuid4().hex[:8]}"
    # Sometimes refresh tokens are rotated, sometimes not. Let's return the same one for simplicity or a new one.
    # We will rotate it here.
    new_refresh_token = f"mock_rt_{uuid.uuid4().hex[:8]}"
    expires_in = 3600

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "Bearer",
        "expires_in": expires_in,
        "scope": "read write",
        "created_at": time.time()
    }
