import pytest
from app import app, tasks


@pytest.fixture
def client():
    # Налаштовуємо тестовий клієнт Flask
    app.config["TESTING"] = True
    tasks.clear()  # Очищуємо список завдань перед кожним тестом
    with app.test_client() as client:
        yield client


def test_create_task(client):
    response = client.post("/tasks", json={"title": "Test Task"})
    assert response.status_code == 201
    assert response.json["title"] == "Test Task"
    assert response.json["id"] == 1


def test_create_task_bad_request(client):
    response = client.post("/tasks", json={})
    assert response.status_code == 400
    assert response.json["error"] == "Title is required"


def test_export_tasks(client):
    # Спочатку створюємо завдання
    client.post("/tasks", json={"title": "Task 1"})

    # Тестуємо експорт
    response = client.get("/tasks/export")
    assert response.status_code == 200
    assert response.json["total"] == 1
    assert len(response.json["tasks"]) == 1