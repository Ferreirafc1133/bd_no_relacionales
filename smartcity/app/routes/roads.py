from fastapi import APIRouter
from app.db.mongo import roads_collection
from datetime import datetime

router = APIRouter()

@router.post("/roads")
def create_road(road: dict):
    road["created_at"] = datetime.utcnow()
    roads_collection.insert_one(road)
    return {"message": "Road created"}

@router.get("/roads")
def get_roads():
    roads = list(roads_collection.find({}, {"_id": 0}))
    return roads
