from fastapi import APIRouter, HTTPException
from app.db.mongo import traffic_data_collection
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/traffic")
def create_traffic_record(record: dict):
    record["timestamp"] = datetime.utcnow()
    result = traffic_data_collection.insert_one(record)
    return {"inserted_id": str(result.inserted_id)}

@router.get("/traffic")
def get_traffic_data():
    data = list(traffic_data_collection.find({}, {"_id": 0}))
    return data

@router.get("/traffic/{traffic_id}")
def get_traffic_by_id(traffic_id: str):
    record = traffic_data_collection.find_one({"_id": ObjectId(traffic_id)})
    if not record:
        raise HTTPException(status_code=404, detail="Traffic record not found")
    record["_id"] = str(record["_id"])
    return record

@router.put("/traffic/{traffic_id}")
def update_traffic_record(traffic_id: str, updated_data: dict):
    result = traffic_data_collection.update_one({"_id": ObjectId(traffic_id)}, {"$set": updated_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Traffic record not found")
    return {"message": "Traffic record updated"}

@router.delete("/traffic/{traffic_id}")
def delete_traffic_record(traffic_id: str):
    result = traffic_data_collection.delete_one({"_id": ObjectId(traffic_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Traffic record not found")
    return {"message": "Traffic record deleted"}
