from flask import Flask, jsonify, request

app = Flask(__name__)

# Тимчасова база даних у пам'яті
tasks = []


@app.route("/")
def home():
    return jsonify({"message": "API is running"}), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    # Валідація: перевіряємо, чи передано заголовок завдання
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "completed": data.get("completed", False),
    }
    tasks.append(task)
    return jsonify(task), 201


@app.route("/tasks/export", methods=["GET"])
def export_tasks():
    return jsonify({"tasks": tasks, "total": len(tasks)}), 200


if __name__ == "__main__":
    app.run(debug=True)