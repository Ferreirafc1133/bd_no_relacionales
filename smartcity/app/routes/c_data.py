from fastapi import APIRouter
from app.db.cassandra import session
from datetime import datetime

router = APIRouter()

### 🚗 TRAFFIC DATA
@router.post("/cassandra/traffic")
def insert_traffic(data: dict):
    session.execute("""
        INSERT INTO traffic_data (road_id, timestamp, vehicle_count, avg_speed)
        VALUES (%s, %s, %s, %s)
    """, (
        data["road_id"], datetime.utcnow(), data["vehicle_count"], data["avg_speed"]
    ))
    return {"message": "Traffic data inserted"}

@router.get("/cassandra/traffic/{road_id}")
def get_traffic(road_id: str):
    result = session.execute("SELECT * FROM traffic_data WHERE road_id=%s", (road_id,))
    return [dict(row._asdict()) for row in result]

@router.delete("/cassandra/traffic/{road_id}")
def delete_traffic(road_id: str):
    session.execute("DELETE FROM traffic_data WHERE road_id=%s", (road_id,))
    return {"message": "Traffic data deleted"}


### ⚡ ENERGY USAGE
@router.post("/cassandra/energy")
def insert_energy(data: dict):
    session.execute("""
        INSERT INTO energy_usage (building_id, timestamp, consumption_kwh)
        VALUES (%s, %s, %s)
    """, (
        data["building_id"], datetime.utcnow(), data["consumption_kwh"]
    ))
    return {"message": "Energy usage inserted"}

@router.get("/cassandra/energy/{building_id}")
def get_energy(building_id: str):
    result = session.execute("SELECT * FROM energy_usage WHERE building_id=%s", (building_id,))
    return [dict(row._asdict()) for row in result]

@router.delete("/cassandra/energy/{building_id}")
def delete_energy(building_id: str):
    session.execute("DELETE FROM energy_usage WHERE building_id=%s", (building_id,))
    return {"message": "Energy usage deleted"}


### 🌡️ CLIMATE DATA
@router.post("/cassandra/climate")
def insert_climate(data: dict):
    session.execute("""
        INSERT INTO climate_data (zone_id, timestamp, temperature, humidity, air_quality)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data["zone_id"], datetime.utcnow(), data["temperature"], data["humidity"], data["air_quality"]
    ))
    return {"message": "Climate data inserted"}

@router.get("/cassandra/climate/{zone_id}")
def get_climate(zone_id: str):
    result = session.execute("SELECT * FROM climate_data WHERE zone_id=%s", (zone_id,))
    return [dict(row._asdict()) for row in result]

@router.delete("/cassandra/climate/{zone_id}")
def delete_climate(zone_id: str):
    session.execute("DELETE FROM climate_data WHERE zone_id=%s", (zone_id,))
    return {"message": "Climate data deleted"}


### 🚨 ALERTS
@router.post("/cassandra/alerts")
def insert_alert(data: dict):
    session.execute("""
        INSERT INTO alerts (alert_type, timestamp, sensor_id, severity, message)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data["alert_type"], datetime.utcnow(), data["sensor_id"], data["severity"], data["message"]
    ))
    return {"message": "Alert inserted"}

@router.get("/cassandra/alerts/{alert_type}")
def get_alerts(alert_type: str):
    result = session.execute("SELECT * FROM alerts WHERE alert_type=%s", (alert_type,))
    return [dict(row._asdict()) for row in result]

@router.delete("/cassandra/alerts/{alert_type}")
def delete_alerts(alert_type: str):
    session.execute("DELETE FROM alerts WHERE alert_type=%s", (alert_type,))
    return {"message": "Alerts deleted"}


### 📟 SENSOR STATUS
@router.post("/cassandra/sensor-status")
def update_sensor_status(data: dict):
    session.execute("""
        INSERT INTO sensor_status (sensor_id, status)
        VALUES (%s, %s)
    """, (
        data["sensor_id"], data["status"]
    ))
    return {"message": "Sensor status updated"}

@router.get("/cassandra/sensor-status/{sensor_id}")
def get_sensor_status(sensor_id: str):
    result = session.execute("SELECT * FROM sensor_status WHERE sensor_id=%s", (sensor_id,))
    return [dict(row._asdict()) for row in result]

@router.delete("/cassandra/sensor-status/{sensor_id}")
def delete_sensor_status(sensor_id: str):
    session.execute("DELETE FROM sensor_status WHERE sensor_id=%s", (sensor_id,))
    return {"message": "Sensor status deleted"}


### 🧾 USER ACTIVITY LOG
@router.post("/cassandra/user-log")
def insert_user_log(data: dict):
    session.execute("""
        INSERT INTO user_activity_log (user_id, timestamp, action, description)
        VALUES (%s, %s, %s, %s)
    """, (
        data["user_id"], datetime.utcnow(), data["action"], data["description"]
    ))
    return {"message": "User log inserted"}

@router.get("/cassandra/user-log/{user_id}")
def get_user_log(user_id: str):
    result = session.execute("SELECT * FROM user_activity_log WHERE user_id=%s", (user_id,))
    return [dict(row._asdict()) for row in result]

@router.delete("/cassandra/user-log/{user_id}")
def delete_user_log(user_id: str):
    session.execute("DELETE FROM user_activity_log WHERE user_id=%s", (user_id,))
    return {"message": "User log deleted"}
