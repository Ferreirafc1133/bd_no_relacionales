from fastapi import APIRouter
from app.db.mongo import traffic_data_collection
from datetime import datetime

router = APIRouter()

@router.post("/traffic")
def create_traffic_record(record: dict):
    record["timestamp"] = datetime.utcnow()
    traffic_data_collection.insert_one(record)
    return {"message": "Traffic record created"}

@router.get("/traffic")
def get_traffic_data():
    data = list(traffic_data_collection.find({}, {"_id": 0}))
    return data
