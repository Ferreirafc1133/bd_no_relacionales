from fastapi import APIRouter, HTTPException
from app.db.mongo import sensors_collection
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/sensors")
def create_sensor(sensor: dict):
    sensor["created_at"] = datetime.utcnow()
    result = sensors_collection.insert_one(sensor)
    return {"inserted_id": str(result.inserted_id)}

@router.get("/sensors")
def get_sensors():
    sensors = list(sensors_collection.find({}, {"_id": 0}))
    return sensors

@router.get("/sensors/{sensor_id}")
def get_sensor_by_id(sensor_id: str):
    sensor = sensors_collection.find_one({"_id": ObjectId(sensor_id)})
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    sensor["_id"] = str(sensor["_id"])
    return sensor

@router.put("/sensors/{sensor_id}")
def update_sensor(sensor_id: str, updated_data: dict):
    result = sensors_collection.update_one({"_id": ObjectId(sensor_id)}, {"$set": updated_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return {"message": "Sensor updated"}

@router.delete("/sensors/{sensor_id}")
def delete_sensor(sensor_id: str):
    result = sensors_collection.delete_one({"_id": ObjectId(sensor_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return {"message": "Sensor deleted"}
