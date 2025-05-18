from fastapi import APIRouter, HTTPException
from app.db.mongo import climate_data_collection
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/climate")
def create_climate_data(data: dict):
    data["timestamp"] = datetime.utcnow()
    result = climate_data_collection.insert_one(data)
    return {"inserted_id": str(result.inserted_id)}

@router.get("/climate")
def get_climate_data():
    data = list(climate_data_collection.find({}, {"_id": 0}))
    return data

@router.put("/climate/{id}")
def update_climate_data(id: str, update_data: dict):
    result = climate_data_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Climate record not found")
    return {"message": "Climate data updated"}

@router.delete("/climate/{id}")
def delete_climate_data(id: str):
    result = climate_data_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Climate record not found")
    return {"message": "Climate data deleted"}
