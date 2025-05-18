from fastapi import APIRouter, HTTPException
from app.db.mongo import energy_usage_collection
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/energy-usage")
def create_energy_usage(data: dict):
    data["timestamp"] = datetime.utcnow()
    result = energy_usage_collection.insert_one(data)
    return {"message": "Energy usage recorded", "id": str(result.inserted_id)}

@router.get("/energy-usage")
def get_energy_usage():
    usage = list(energy_usage_collection.find({}, {"_id": 0}))
    return usage

@router.put("/energy-usage/{id}")
def update_energy_usage(id: str, update_data: dict):
    result = energy_usage_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Energy usage updated"}

@router.delete("/energy-usage/{id}")
def delete_energy_usage(id: str):
    result = energy_usage_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Energy usage deleted"}
