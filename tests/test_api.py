from NNTouristsAPI import api
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
async def test_get_random_rows():
    async with AsyncClient(transport=ASGITransport(app=api.app), base_url="http://test") as aclient:
        response = await aclient.get("/random_rows/10")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10

@pytest.mark.asyncio
async def test_get_sorted_by_month():
    async with AsyncClient(transport=ASGITransport(app=api.app), base_url="http://test") as aclient:
        response = await aclient.get("/count_sort/month")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 12

@pytest.mark.asyncio
async def test_get_sorted_by_trip_type():
    async with AsyncClient(transport=ASGITransport(app=api.app), base_url="http://test") as aclient:
        response = await aclient.get("/count_sort/trip_type")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

@pytest.mark.asyncio
async def test_get_sorted_by_visit_type():
    async with AsyncClient(transport=ASGITransport(app=api.app), base_url="http://test") as aclient:
        response = await aclient.get("/count_sort/visit_type")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

@pytest.mark.asyncio
async def test_get_sorted_by_goal():
    async with AsyncClient(transport=ASGITransport(app=api.app), base_url="http://test") as aclient:
        response = await aclient.get("/count_sort/goal")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

@pytest.mark.asyncio
async def test_get_sorted_by_gender():
    async with AsyncClient(transport=ASGITransport(app=api.app), base_url="http://test") as aclient:
        response = await aclient.get("/count_sort/gender")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

@pytest.mark.asyncio
async def test_get_sorted_by_tourist_age():
    async with AsyncClient(transport=ASGITransport(app=api.app), base_url="http://test") as aclient:
        response = await aclient.get("/count_sort/tourist_age")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 8

@pytest.mark.asyncio
async def test_get_sorted_by_income():
    async with AsyncClient(transport=ASGITransport(app=api.app), base_url="http://test") as aclient:
        response = await aclient.get("/count_sort/income")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 6

@pytest.mark.asyncio
async def test_get_sorted_by_geo_home_country():
    async with AsyncClient(transport=ASGITransport(app=api.app), base_url="http://test") as aclient:
        response = await aclient.get("/count_sort_geo/home_country")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 106

@pytest.mark.asyncio
async def test_get_sorted_by_geo_home_region():
    async with AsyncClient(transport=ASGITransport(app=api.app), base_url="http://test") as aclient:
        response = await aclient.get("/count_sort_geo/home_region")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 84

@pytest.mark.asyncio
async def test_get_sorted_by_geo_home_city():
    async with AsyncClient(transport=ASGITransport(app=api.app), base_url="http://test") as aclient:
        response = await aclient.get("/count_sort_geo/home_city")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 52

@pytest.mark.asyncio
async def test_cohort_analytic_home_region():
    async with AsyncClient(transport=ASGITransport(app=api.app), base_url="http://test") as aclient:
        response = await aclient.get("/cohort_geo/home_region")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 84

@pytest.mark.asyncio
async def test_cohort_analytic_home_city():
    async with AsyncClient(transport=ASGITransport(app=api.app), base_url="http://test") as aclient:
        response = await aclient.get("/cohort_geo/home_city")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 52

@pytest.mark.asyncio
async def test_avg_values():
    async with AsyncClient(transport=ASGITransport(app=api.app), base_url="http://test") as aclient:
        response = await aclient.get("/avg_values")
        assert response.status_code == 200