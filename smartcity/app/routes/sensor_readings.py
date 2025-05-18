from fastapi import APIRouter, HTTPException
from app.db.mongo import sensor_readings_collection
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/sensor-readings")
def create_sensor_reading(data: dict):
    data["timestamp"] = datetime.utcnow()
    result = sensor_readings_collection.insert_one(data)
    return {"inserted_id": str(result.inserted_id)}

@router.get("/sensor-readings")
def get_sensor_readings():
    readings = list(sensor_readings_collection.find({}, {"_id": 0}))
    return readings

@router.get("/sensor-readings/{reading_id}")
def get_sensor_reading_by_id(reading_id: str):
    reading = sensor_readings_collection.find_one({"_id": ObjectId(reading_id)})
    if not reading:
        raise HTTPException(status_code=404, detail="Sensor reading not found")
    reading["_id"] = str(reading["_id"])
    return reading

@router.put("/sensor-readings/{reading_id}")
def update_sensor_reading(reading_id: str, updated_data: dict):
    result = sensor_readings_collection.update_one({"_id": ObjectId(reading_id)}, {"$set": updated_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Sensor reading not found")
    return {"message": "Sensor reading updated"}

@router.delete("/sensor-readings/{reading_id}")
def delete_sensor_reading(reading_id: str):
    result = sensor_readings_collection.delete_one({"_id": ObjectId(reading_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sensor reading not found")
    return {"message": "Sensor reading deleted"}
