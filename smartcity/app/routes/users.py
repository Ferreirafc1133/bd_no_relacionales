# routes/users.py
from fastapi import APIRouter
from app.db.mongo import users_collection
from datetime import datetime

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
