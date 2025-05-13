from fastapi import APIRouter
from app.db.mongo import buildings_collection
from datetime import datetime

router = APIRouter()

@router.post("/buildings")
def create_building(building: dict):
    building["created_at"] = datetime.utcnow()
    buildings_collection.insert_one(building)
    return {"message": "Building created"}

@router.get("/buildings")
def get_buildings():
    buildings = list(buildings_collection.find({}, {"_id": 0}))
    return buildings
