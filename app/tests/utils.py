from datetime import datetime, timedelta
from ..utils.auth import create_access_token

def get_test_token(username, minutes=30):
    """Generate a test token for authentication"""
    access_token_expires = timedelta(minutes=minutes)
    return create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )

def get_auth_headers(token):
    """Get authorization headers with the given token"""
    return {"Authorization": f"Bearer {token}"}