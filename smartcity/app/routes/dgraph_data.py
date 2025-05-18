from fastapi import APIRouter
from app.db.dgraph import client
from datetime import datetime
import json

router = APIRouter()

def run_mutation(data: dict):
    txn = client.txn()
    try:
        res = txn.mutate(set_obj=data)
        txn.commit()
        return res.uids
    finally:
        txn.discard()

### 👤 CREATE USER + LOG
@router.post("/dgraph/users")
def create_user_with_log(data: dict):
    user = {
        "dgraph.type": "User",
        "name": data["name"],
        "email": data["email"],
        "role": data["role"],
        "performed": [
            {
                "dgraph.type": "Log",
                "action": data["log_action"],
                "timestamp": datetime.utcnow().isoformat(),
                "description": data["log_description"]
            }
        ]
    }
    return run_mutation(user)

@router.put("/dgraph/users/{uid}")
def update_user(uid: str, data: dict):
    return run_mutation({
        "uid": uid,
        "name": data.get("name"),
        "email": data.get("email"),
        "role": data.get("role")
    })

@router.delete("/dgraph/users/{uid}")
def delete_user(uid: str):
    txn = client.txn()
    try:
        txn.mutate(del_obj={"uid": uid})
        txn.commit()
        return {"message": f"User {uid} deleted"}
    finally:
        txn.discard()

@router.get("/dgraph/users")
def get_users():
    query = """
    {
        users(func: type(User)) {
            uid
            name
            email
            role
            performed {
                action
                timestamp
                description
            }
        }
    }
    """
    res = client.txn(read_only=True).query(query)
    return json.loads(res.json).get("users", [])

### 🏢 BUILDINGS
@router.post("/dgraph/buildings")
def create_building(data: dict):
    building = {
        "dgraph.type": "Building",
        "name": data["name"],
        "type": data["type"],
        "location_lat": data["lat"],
        "location_lon": data["lon"],
        "zone": data["zone"]
    }
    return run_mutation(building)

@router.put("/dgraph/buildings/{uid}")
def update_building(uid: str, data: dict):
    return run_mutation({
        "uid": uid,
        "name": data.get("name"),
        "type": data.get("type"),
        "location_lat": data.get("lat"),
        "location_lon": data.get("lon"),
        "zone": data.get("zone")
    })

@router.delete("/dgraph/buildings/{uid}")
def delete_building(uid: str):
    txn = client.txn()
    try:
        txn.mutate(del_obj={"uid": uid})
        txn.commit()
        return {"message": f"Building {uid} deleted"}
    finally:
        txn.discard()

@router.get("/dgraph/buildings")
def get_buildings():
    query = """
    {
        buildings(func: type(Building)) {
            uid
            name
            type
            location_lat
            location_lon
            zone
        }
    }
    """
    res = client.txn(read_only=True).query(query)
    return json.loads(res.json).get("buildings", [])

### 📡 SENSORS
@router.post("/dgraph/sensors")
def create_sensor(data: dict):
    return run_mutation({
        "dgraph.type": "Sensor",
        "type": data["type"],
        "status": data["status"],
        "location_lat": data["lat"],
        "location_lon": data["lon"],
        "zone": data["zone"],
        "installedIn": {"uid": data["building_uid"]},
        "poweredBy": {"uid": data["power_node_uid"]}
    })

@router.put("/dgraph/sensors/{uid}")
def update_sensor(uid: str, data: dict):
    return run_mutation({
        "uid": uid,
        "type": data.get("type"),
        "status": data.get("status"),
        "location_lat": data.get("lat"),
        "location_lon": data.get("lon"),
        "zone": data.get("zone"),
        "installedIn": {"uid": data.get("building_uid")},
        "poweredBy": {"uid": data.get("power_node_uid")}
    })

@router.delete("/dgraph/sensors/{uid}")
def delete_sensor(uid: str):
    txn = client.txn()
    try:
        txn.mutate(del_obj={"uid": uid})
        txn.commit()
        return {"message": f"Sensor {uid} deleted"}
    finally:
        txn.discard()

@router.get("/dgraph/sensors")
def get_sensors():
    query = """
    {
        sensors(func: type(Sensor)) {
            uid
            type
            status
            location_lat
            location_lon
            zone
            installedIn {
                uid
                name
            }
            poweredBy {
                uid
                type
            }
        }
    }
    """
    res = client.txn(read_only=True).query(query)
    return json.loads(res.json).get("sensors", [])

### ⚡ POWER NODES
@router.post("/dgraph/power-nodes")
def create_power_node(data: dict):
    return run_mutation({
        "dgraph.type": "PowerNode",
        "type": data["type"],
        "status": data["status"],
        "zone": data["zone"]
    })

@router.put("/dgraph/power-nodes/{uid}")
def update_power_node(uid: str, data: dict):
    return run_mutation({
        "uid": uid,
        "type": data.get("type"),
        "status": data.get("status"),
        "zone": data.get("zone")
    })

@router.delete("/dgraph/power-nodes/{uid}")
def delete_power_node(uid: str):
    txn = client.txn()
    try:
        txn.mutate(del_obj={"uid": uid})
        txn.commit()
        return {"message": f"PowerNode {uid} deleted"}
    finally:
        txn.discard()

@router.get("/dgraph/power-nodes")
def get_power_nodes():
    query = """
    {
        powerNodes(func: type(PowerNode)) {
            uid
            type
            status
            zone
        }
    }
    """
    res = client.txn(read_only=True).query(query)
    return json.loads(res.json).get("powerNodes", [])

### 📈 SENSOR READINGS
@router.post("/dgraph/sensor-readings")
def create_reading(data: dict):
    return run_mutation({
        "dgraph.type": "SensorReading",
        "value": data["value"],
        "type": data["type"],
        "timestamp": datetime.utcnow().isoformat(),
        "readingOf": {"uid": data["sensor_uid"]}
    })

@router.put("/dgraph/sensor-readings/{uid}")
def update_reading(uid: str, data: dict):
    return run_mutation({
        "uid": uid,
        "value": data.get("value"),
        "type": data.get("type"),
        "timestamp": datetime.utcnow().isoformat(),
        "readingOf": {"uid": data.get("sensor_uid")}
    })

@router.delete("/dgraph/sensor-readings/{uid}")
def delete_reading(uid: str):
    txn = client.txn()
    try:
        txn.mutate(del_obj={"uid": uid})
        txn.commit()
        return {"message": f"Reading {uid} deleted"}
    finally:
        txn.discard()

@router.get("/dgraph/sensor-readings")
def get_sensor_readings():
    query = """
    {
        readings(func: type(SensorReading)) {
            uid
            value
            type
            timestamp
            readingOf {
                uid
                type
            }
        }
    }
    """
    res = client.txn(read_only=True).query(query)
    return json.loads(res.json).get("readings", [])
