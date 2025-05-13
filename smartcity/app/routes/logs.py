from fastapi import APIRouter
from app.db.mongo import logs_collection
from datetime import datetime

router = APIRouter()

@router.post("/logs")
def create_log(log: dict):
    log["timestamp"] = datetime.utcnow()
    logs_collection.insert_one(log)
    return {"message": "Log saved"}

@router.get("/logs")
def get_logs():
    logs = list(logs_collection.find({}, {"_id": 0}))
    return logs
