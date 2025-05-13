from fastapi import APIRouter
from app.db.mongo import users_collection, sensors_collection

router = APIRouter()

@router.get("/mongo/aggregations")
def mongo_aggregations():
    avg_temp = sensors_collection.aggregate([
        {"$match": {"type": "temperature"}},
        {"$group": {"_id": None, "avg_temp": {"$avg": {"$toDouble": "$location.lat"}}}}
    ])
    
    total_users = users_collection.count_documents({})

    return {
        "avg_sensor_latitude_temp_type": list(avg_temp),
        "total_users": total_users
    }
