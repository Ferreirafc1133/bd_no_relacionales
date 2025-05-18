from fastapi import APIRouter, HTTPException
from app.db.mongo import logs_collection
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/logs")
def create_log(log: dict):
    log["timestamp"] = datetime.utcnow()
    result = logs_collection.insert_one(log)
    return {"message": "Log saved", "id": str(result.inserted_id)}

@router.get("/logs")
def get_logs():
    logs = list(logs_collection.find({}, {"_id": 0}))
    return logs

@router.put("/logs/{id}")
def update_log(id: str, update_data: dict):
    result = logs_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Log not found")
    return {"message": "Log updated"}

@router.delete("/logs/{id}")
def delete_log(id: str):
    result = logs_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Log not found")
    return {"message": "Log deleted"}
