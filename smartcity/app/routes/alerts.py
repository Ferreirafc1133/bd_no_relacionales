from fastapi import APIRouter
from app.db.mongo import alerts_collection
from datetime import datetime

router = APIRouter()

@router.post("/alerts")
def create_alert(alert: dict):
    alert["timestamp"] = datetime.utcnow()
    alerts_collection.insert_one(alert)
    return {"message": "Alert created"}

@router.get("/alerts")
def get_alerts():
    alerts = list(alerts_collection.find({}, {"_id": 0}))
    return alerts
