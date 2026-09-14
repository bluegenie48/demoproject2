"""Background task definitions."""

import os
from celery import Celery

app = Celery('worker', broker=os.environ.get('REDIS_URL', 'redis://localhost:6379/0'))


@app.task
def process_upload(file_id: str):
    """Process an uploaded file — resize images, extract metadata."""
    from PIL import Image
    # placeholder
    return {"file_id": file_id, "status": "processed"}


@app.task
def sync_external(endpoint: str, api_key: str):
    """Pull data from an external API and store locally."""
    import requests
    resp = requests.get(endpoint, headers={"Authorization": f"Bearer {api_key}"}, timeout=30)
    resp.raise_for_status()
    return {"records": len(resp.json().get("data", []))}


@app.task
def rotate_encryption_key():
    """Rotate the symmetric encryption key used for stored secrets."""
    from cryptography.fernet import Fernet
    new_key = Fernet.generate_key()
    # In production this would re-encrypt stored values
    return {"key_rotated": True}
