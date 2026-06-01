from httpx import ASGITransport, AsyncClient
import pytest

from app.main import app


@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_health(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_todo(client):
    resp = await client.post("/api/todos", json={"title": "test todo"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "test todo"
    assert data["completed"] is False
    assert data["id"] == 1


@pytest.mark.asyncio
async def test_list_todos(client):
    resp = await client.get("/api/todos")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_get_todo_not_found(client):
    resp = await client.get("/api/todos/999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_todo(client):
    await client.post("/api/todos", json={"title": "todo to update"})
    resp = await client.put("/api/todos/2", json={"title": "updated", "completed": True})
    assert resp.status_code == 200
    assert resp.json()["title"] == "updated"
    assert resp.json()["completed"] is True


@pytest.mark.asyncio
async def test_delete_todo(client):
    await client.post("/api/todos", json={"title": "todo to delete"})
    resp = await client.delete("/api/todos/3")
    assert resp.status_code == 200
    resp = await client.get("/api/todos/3")
    assert resp.status_code == 404
