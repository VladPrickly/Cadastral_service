import pytest
import respx
from httpx import Response


@pytest.mark.asyncio
async def test_ping_endpoint(client):
    response = await client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
@respx.mock
async def test_query_endpoint(client):
    external_url = "http://localhost:8000/result"
    respx.get(external_url).mock(return_value=Response(200, json={"result": True}))
    payload = {
        "cadastral_number": "77:01:9999999:111",
        "latitude": 55.66,
        "longitude": 77.88
    }

    response = await client.post("/query", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert data["cadastral_number"] == "77:01:9999999:111"
    assert data["latitude"] == 55.66
    assert data["longitude"] == 77.88
    assert "id" in data
    assert "result" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_history_endpoint(client):
    response = await client.get("/history")

    assert response.status_code == 200
    assert isinstance(response.json(), list)