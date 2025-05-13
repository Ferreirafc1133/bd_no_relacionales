from fastapi import APIRouter
from app.db.mongo import climate_data_collection
from datetime import datetime

router = APIRouter()

@router.post("/climate")
def create_climate_data(data: dict):
    data["timestamp"] = datetime.utcnow()
    climate_data_collection.insert_one(data)
    return {"message": "Climate data recorded"}

@router.get("/climate")
def get_climate_data():
    data = list(climate_data_collection.find({}, {"_id": 0}))
    return data
