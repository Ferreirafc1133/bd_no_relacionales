from fastapi import APIRouter, HTTPException
from app.db.mongo import alerts_collection
from datetime import datetime
from bson import ObjectId

router = APIRouter()

# 📥 Crear alerta
@router.post("/alerts")
def create_alert(alert: dict):
    alert["timestamp"] = datetime.utcnow()
    result = alerts_collection.insert_one(alert)
    return {"message": "Alert created", "id": str(result.inserted_id)}

# 📤 Obtener todas las alertas
@router.get("/alerts")
def get_alerts():
    alerts = list(alerts_collection.find({}, {"_id": 0}))
    return alerts

# 🔍 Obtener alerta por ID
@router.get("/alerts/{alert_id}")
def get_alert(alert_id: str):
    alert = alerts_collection.find_one({"_id": ObjectId(alert_id)})
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert["_id"] = str(alert["_id"])
    return alert

# ✏️ Editar alerta por ID
@router.put("/alerts/{alert_id}")
def update_alert(alert_id: str, updated: dict):
    result = alerts_collection.update_one(
        {"_id": ObjectId(alert_id)},
        {"$set": updated}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"message": "Alert updated"}

# 🗑️ Borrar alerta por ID
@router.delete("/alerts/{alert_id}")
def delete_alert(alert_id: str):
    result = alerts_collection.delete_one({"_id": ObjectId(alert_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"message": "Alert deleted"}
