import pytest
from httpx import ASGITransport, AsyncClient
from src.main import app

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

async def test_get_existed_user(client):
    await client.post("/users", json={"name": "Existed", "email": "existed@test.com"})
    response = await client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

async def test_create_user(client):
    response = await client.post("/users", json={"name": "Test", "email": "test@test.com"})
    assert response.status_code == 201

async def test_get_not_existed_user(client):
    response = await client.get("/users/999999")
    assert response.status_code == 404

async def test_update_user(client):
    created = (await client.post("/users", json={"name": "Old", "email": "old@test.com"})).json()
    response = await client.put(f"/users/{created['id']}", json={"name": "New", "email": "new@test.com"})
    assert response.status_code == 200
    assert response.json()["name"] == "New"

async def test_delete_user(client):
    created = (await client.post("/users", json={"name": "ToDelete", "email": "del@test.com"})).json()
    response = await client.delete(f"/users/{created['id']}")
    assert response.status_code == 204
