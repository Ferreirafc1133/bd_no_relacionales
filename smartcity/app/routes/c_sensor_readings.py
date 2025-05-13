from fastapi import APIRouter
from app.db.cassandra import session
from datetime import datetime

router = APIRouter()

@router.post("/cassandra/sensor-readings")
def insert_sensor_reading(data: dict):
    session.execute("""
        INSERT INTO sensor_readings (sensor_id, timestamp, type, value)
        VALUES (%s, %s, %s, %s)
    """, (
        data["sensor_id"],
        datetime.utcnow(),
        data["type"],
        data["value"]
    ))
    return {"message": "Reading inserted in Cassandra"}

@router.get("/cassandra/sensor-readings/{sensor_id}")
def get_sensor_readings(sensor_id: str):
    result = session.execute("""
        SELECT * FROM sensor_readings WHERE sensor_id=%s
    """, (sensor_id,))
    return [dict(row._asdict()) for row in result]
