import json
import sqlite3
from pathlib import Path
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config["DB_PATH"] = "tasks.db"
app.config["EXPORT_PATH"] = "tasks.json"


def get_db():
    conn = sqlite3.connect(app.config["DB_PATH"])
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL
            )
            """
        )


def export_tasks(filepath=None):
    target = Path(filepath or app.config["EXPORT_PATH"])
    with get_db() as conn:
        rows = conn.execute("SELECT id, title FROM tasks ORDER BY id").fetchall()
    tasks = [{"id": row["id"], "title": row["title"]} for row in rows]
    target.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")
    return tasks


def load_tasks(filepath):
    return json.loads(Path(filepath).read_text(encoding="utf-8"))


@app.get("/tasks")
def get_tasks():
    with get_db() as conn:
        rows = conn.execute("SELECT id, title FROM tasks ORDER BY id").fetchall()
    return jsonify([{"id": r["id"], "title": r["title"]} for r in rows]), 200


@app.post("/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    if not title or not str(title).strip():
        return jsonify({"error": "Field 'title' is required"}), 400

    with get_db() as conn:
        cursor = conn.execute("INSERT INTO tasks (title) VALUES (?)", (title.strip(),))
        task_id = cursor.lastrowid

    export_tasks()
    return jsonify({"id": task_id, "title": title.strip()}), 201


# 🔥 Завдання підвищеної складності: маршрут видалення
@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if cursor.rowcount == 0:
            return jsonify({"error": "Task not found"}), 404

    export_tasks()
    return jsonify({"status": "deleted", "id": task_id}), 200


if __name__ == "__main__":
    init_db()
    app.run(debug=True)