from fastapi import APIRouter, HTTPException
from app.db.mongo import roads_collection
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/roads")
def create_road(road: dict):
    road["created_at"] = datetime.utcnow()
    result = roads_collection.insert_one(road)
    return {"inserted_id": str(result.inserted_id)}

@router.get("/roads")
def get_roads():
    roads = list(roads_collection.find({}, {"_id": 0}))
    return roads

@router.get("/roads/{road_id}")
def get_road_by_id(road_id: str):
    road = roads_collection.find_one({"_id": ObjectId(road_id)})
    if not road:
        raise HTTPException(status_code=404, detail="Road not found")
    road["_id"] = str(road["_id"])
    return road

@router.put("/roads/{road_id}")
def update_road(road_id: str, updated_data: dict):
    result = roads_collection.update_one({"_id": ObjectId(road_id)}, {"$set": updated_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Road not found")
    return {"message": "Road updated"}

@router.delete("/roads/{road_id}")
def delete_road(road_id: str):
    result = roads_collection.delete_one({"_id": ObjectId(road_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Road not found")
    return {"message": "Road deleted"}
