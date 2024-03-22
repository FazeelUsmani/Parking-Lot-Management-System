import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from app.main import app
from app.config import settings
from app.database import get_slot_collection
from pymongo import MongoClient

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(autouse=True)
async def setup_and_teardown_db():
    settings.database_name = "test_parking_lot"
    client = MongoClient(settings.database_url)
    db = client[settings.database_name]
    yield
    client.drop_database("test_parking_lot")
    client.close()

# Test parking a car
@pytest.mark.asyncio
async def test_park_car(client):
    response = await client.post("/parking/park", json={"car_number": "AP11AK1264"})  
    assert response.status_code == 201
    assert response.json()["car_number"] == "AP11AK1264"
    assert "slot_number" in response.json()

# Test unparking a car
@pytest.mark.asyncio
async def test_unpark_car(client, setup_and_teardown_db):
    slots_collection = get_slot_collection()
    slots_collection.insert_one({"car_number": "AP11AK1264", "slot_number": 1})
    response = await client.delete("/parking/unpark/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Car AP11AK1264 has been removed from slot 1"}

# Test getting car/slot information
@pytest.mark.asyncio
async def test_get_info(client, setup_and_teardown_db):
    slots_collection = get_slot_collection()
    slots_collection.insert_one({"car_number": "AP11AK1264", "slot_number": 1})
    response = await client.get("/parking/getinfo?car_number=AP11AK1264")
    assert response.status_code == 200
    assert response.json() == {"car_number": "AP11AK1264", "slot_number": 1}
