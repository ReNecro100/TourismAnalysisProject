import api
import pytest
from httpx import AsyncClient, ASGITransport

#pytest -s

@pytest.mark.asyncio
async def test_read_root():
    async with AsyncClient(transport=ASGITransport(app=api.app), base_url="http://test") as aclient:
        response = await aclient.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data == {"message": "Yeah, that's Nizhny Novgorod 2022 Tourists API"}

@pytest.mark.asyncio
async def test_random_rows():
    async with AsyncClient(transport=ASGITransport(app=api.app), base_url="http://test") as aclient:
        response = await aclient.get("/random_rows/10")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10