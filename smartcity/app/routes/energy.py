from fastapi import APIRouter
from app.db.mongo import energy_usage_collection
from datetime import datetime

router = APIRouter()

@router.post("/energy-usage")
def create_energy_usage(data: dict):
    data["timestamp"] = datetime.utcnow()
    energy_usage_collection.insert_one(data)
    return {"message": "Energy usage recorded"}

@router.get("/energy-usage")
def get_energy_usage():
    usage = list(energy_usage_collection.find({}, {"_id": 0}))
    return usage
