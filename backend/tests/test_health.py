"""
Tests for the health module
"""

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

# pytest fixture — like beforeEach in Vitest
# It creates a test HTTP client that talks directly to my FastAPI app (main.py)
# without needing a real server running
# "function" scope means a fresh client per test function
@pytest.fixture
async def client():
    # ASGITransport lets httpx talk to a FastAPI app directly in memory
    # In TS (Vitest) we'd use supertest(app)
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac: # ac is the AsyncClient instance
        yield ac # yield is like return but keeps the context alive for the test

# Tests are just async functions prefixed with test_
# pytest finds them automatically (like Vitest's it/describe)
async def test_health_check_returns_200(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")

    assert response.status_code == 200

async def test_health_check_returns_correct_shape(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")
    data = response.json()

    assert data["status"] == "ok"
    assert "version" in data
    assert "timestamp" in data

async def test_root_endpoint(client: AsyncClient) -> None:
    response = await client.get("/")

    assert response.status_code == 200
    assert "running" in response.json()["message"]