import json
import sqlite3
import pytest
from app import app, init_db, export_tasks, load_tasks


@pytest.fixture
def client(tmp_path):
    """Створює ізольоване середовище (окрему БД і JSON) для кожного тесту."""
    db_file = tmp_path / "test_tasks.db"
    export_file = tmp_path / "test_tasks.json"

    app.config["TESTING"] = True
    app.config["DB_PATH"] = str(db_file)
    app.config["EXPORT_PATH"] = str(export_file)

    init_db()
    with app.test_client() as test_client:
        yield test_client


# ==========================================
# КРОК 2: Тестування файлів (export_tasks)
# ==========================================

def test_export_empty_list(client, tmp_path):
    """⭐ Перевірка експорту порожнього списку завдань."""
    export_file = tmp_path / "empty.json"
    export_tasks(export_file)

    assert export_file.exists()
    data = json.loads(export_file.read_text(encoding="utf-8"))
    assert data == []


def test_corrupted_json_file(tmp_path):
    """⭐ Перевірка обробки пошкодженого JSON-файлу."""
    bad_file = tmp_path / "corrupted.json"
    bad_file.write_text("{broken json: [1, 2,", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        load_tasks(bad_file)


# ==========================================
# КРОК 3: Тестування бази даних (SQLite)
# ==========================================

def test_db_table_created(client):
    """Перевірка, що init_db створює таблицю tasks у SQLite."""
    conn = sqlite3.connect(app.config["DB_PATH"])
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'"
    )
    assert cursor.fetchone() is not None
    conn.close()


def test_tasks_order_in_db(client):
    """⭐ Створення двох завдань і перевірка їхнього порядку в БД."""
    client.post("/tasks", json={"title": "Перше завдання"})
    client.post("/tasks", json={"title": "Друге завдання"})

    conn = sqlite3.connect(app.config["DB_PATH"])
    rows = conn.execute("SELECT id, title FROM tasks ORDER BY id").fetchall()
    conn.close()

    assert len(rows) == 2
    assert rows[0] == (1, "Перше завдання")
    assert rows[1] == (2, "Друге завдання")


# ==========================================
# КРОК 4: Тестування вебзастосунку (Flask)
# ==========================================

def test_create_and_get_task(client):
    """Інтеграційний сценарій: HTTP POST -> SQLite -> JSON -> HTTP GET."""
    response = client.post("/tasks", json={"title": "Вивчити pytest"})
    assert response.status_code == 201
    created = response.get_json()
    assert created["title"] == "Вивчити pytest"

    # Перевірка GET (статус 200)
    get_resp = client.get("/tasks")
    assert get_resp.status_code == 200
    assert len(get_resp.get_json()) == 1

    # Перевірка JSON-файлу на диску
    exported = json.loads(open(app.config["EXPORT_PATH"], encoding="utf-8").read())
    assert exported[0]["title"] == "Вивчити pytest"


def test_create_task_without_title_returns_400(client):
    """⭐ Перевірка POST-запиту без поля title (очікуємо статус 400)."""
    response = client.post("/tasks", json={})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_delete_task_integration(client):
    """🔥 Повний інтеграційний тест видалення завдання (HTTP + БД + JSON)."""
    # 1. Створюємо завдання
    create_resp = client.post("/tasks", json={"title": "Тимчасове завдання"})
    task_id = create_resp.get_json()["id"]

    # 2. Видаляємо його через DELETE
    del_resp = client.delete(f"/tasks/{task_id}")
    assert del_resp.status_code == 200

    # 3. Перевіряємо, що запис зник із SQLite
    conn = sqlite3.connect(app.config["DB_PATH"])
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    assert row is None

    # 4. Перевіряємо, що JSON-файл оновився і тепер порожній
    exported = json.loads(open(app.config["EXPORT_PATH"], encoding="utf-8").read())
    assert exported == []