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


### 🏢 CREATE BUILDING
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


### 📡 CREATE SENSOR and link to BUILDING and POWER NODE
@router.post("/dgraph/sensors")
def create_sensor(data: dict):
    sensor = {
        "dgraph.type": "Sensor",
        "type": data["type"],
        "status": data["status"],
        "location_lat": data["lat"],
        "location_lon": data["lon"],
        "zone": data["zone"],
        "installedIn": {"uid": data["building_uid"]},
        "poweredBy": {"uid": data["power_node_uid"]}
    }
    return run_mutation(sensor)


### ⚡ CREATE POWER NODE
@router.post("/dgraph/power-nodes")
def create_power_node(data: dict):
    node = {
        "dgraph.type": "PowerNode",
        "type": data["type"],
        "status": data["status"],
        "zone": data["zone"]
    }
    return run_mutation(node)


### 📈 CREATE SENSOR READING
@router.post("/dgraph/sensor-readings")
def create_reading(data: dict):
    reading = {
        "dgraph.type": "SensorReading",
        "value": data["value"],
        "type": data["type"],
        "timestamp": datetime.utcnow().isoformat(),
        "readingOf": {"uid": data["sensor_uid"]}
    }
    return run_mutation(reading)

### GET USERS
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


### GET BUILDINGS
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


### GET SENSORS
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


### GET POWER NODES
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


### GET SENSOR READINGS
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
