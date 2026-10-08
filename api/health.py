"""Health check endpoint for load balancer probes."""

from flask import jsonify
from api.search import app


@app.route("/api/health")
def health():
    """Return service health status."""
    return jsonify({"status": "ok", "version": "0.3.4"})
