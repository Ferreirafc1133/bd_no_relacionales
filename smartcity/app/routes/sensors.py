from fastapi import APIRouter
from app.db.mongo import sensors_collection
from datetime import datetime

router = APIRouter()

@router.post("/sensors")
def create_sensor(sensor: dict):
    sensor["created_at"] = datetime.utcnow()
    sensors_collection.insert_one(sensor)
    return {"message": "Sensor created"}

@router.get("/sensors")
def get_sensors():
    sensors = list(sensors_collection.find({}, {"_id": 0}))
    return sensors
