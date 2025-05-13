from fastapi import APIRouter
from app.db.mongo import sensor_readings_collection
from datetime import datetime

router = APIRouter()

@router.post("/sensor-readings")
def create_sensor_reading(data: dict):
    data["timestamp"] = datetime.utcnow()
    sensor_readings_collection.insert_one(data)
    return {"message": "Sensor reading created"}

@router.get("/sensor-readings")
def get_sensor_readings():
    readings = list(sensor_readings_collection.find({}, {"_id": 0}))
    return readings
