from fastapi import APIRouter, HTTPException
from app.db.mongo import users_collection
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/users")
def create_user(user: dict):
    user["created_at"] = datetime.utcnow()
    result = users_collection.insert_one(user)
    return {"inserted_id": str(result.inserted_id)}

@router.get("/users")
def get_users():
    users = list(users_collection.find({}, {"_id": 0}))
    return users

@router.get("/users/{user_id}")
def get_user_by_id(user_id: str):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["_id"] = str(user["_id"])
    return user

@router.put("/users/{user_id}")
def update_user(user_id: str, updated_data: dict):
    result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated"}

@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
