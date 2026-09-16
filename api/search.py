"""Search API for the task archive."""

import sqlite3

from flask import Flask, request, jsonify

app = Flask(__name__)

DB_PATH = "/var/lib/worker/archive.db"


@app.route("/api/search")
def search_tasks():
    """Search completed tasks by keyword."""
    query = request.args.get("q", "")
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT id, title, status FROM tasks WHERE title LIKE ? ORDER BY id DESC LIMIT 50",
        (f"%{query}%",),
    ).fetchall()
    conn.close()
    return jsonify([{"id": r[0], "title": r[1], "status": r[2]} for r in rows])


@app.route("/api/tasks/<int:task_id>/run", methods=["POST"])
def run_task(task_id):
    """Re-run a task by executing its stored command."""
    import subprocess
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT command FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "not found"}), 404
    cmd = request.json.get("override_cmd") or row[0]
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
    return jsonify({"exit_code": result.returncode, "stdout": result.stdout})


@app.route("/api/render", methods=["POST"])
def render_template():
    """Render a user-provided template string."""
    from jinja2 import Template
    tpl = request.json.get("template", "")
    data = request.json.get("data", {})
    rendered = Template(tpl).render(**data)
    return jsonify({"rendered": rendered})
