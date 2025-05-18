from fastapi import APIRouter, HTTPException
from app.db.mongo import buildings_collection
from datetime import datetime
from bson import ObjectId

router = APIRouter()

# 🏗️ Crear edificio
@router.post("/buildings")
def create_building(building: dict):
    building["created_at"] = datetime.utcnow()
    result = buildings_collection.insert_one(building)
    return {"message": "Building created", "id": str(result.inserted_id)}

# 🧱 Obtener todos los edificios
@router.get("/buildings")
def get_buildings():
    buildings = list(buildings_collection.find({}, {"_id": 0}))
    return buildings

# 🔍 Obtener edificio por ID
@router.get("/buildings/{building_id}")
def get_building(building_id: str):
    building = buildings_collection.find_one({"_id": ObjectId(building_id)})
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    building["_id"] = str(building["_id"])
    return building

# ✏️ Editar edificio por ID
@router.put("/buildings/{building_id}")
def update_building(building_id: str, updated: dict):
    result = buildings_collection.update_one(
        {"_id": ObjectId(building_id)},
        {"$set": updated}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Building not found")
    return {"message": "Building updated"}

# 🗑️ Borrar edificio por ID
@router.delete("/buildings/{building_id}")
def delete_building(building_id: str):
    result = buildings_collection.delete_one({"_id": ObjectId(building_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Building not found")
    return {"message": "Building deleted"}
