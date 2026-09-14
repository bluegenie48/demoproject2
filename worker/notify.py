"""Notification helpers for completed tasks."""

import requests


def send_webhook(url: str, payload: dict):
    """POST a JSON payload to a webhook endpoint."""
    resp = requests.post(url, json=payload, timeout=10)
    resp.raise_for_status()
    return resp.status_code


def send_alert(channel: str, message: str):
    """Send an alert to a monitoring channel."""
    # placeholder for Slack/Discord integration
    return {"channel": channel, "sent": True}
