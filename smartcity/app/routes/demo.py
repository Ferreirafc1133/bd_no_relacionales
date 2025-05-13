from fastapi import APIRouter
from app.db.mongo import (
    users_collection, buildings_collection, roads_collection,
    sensors_collection, sensor_readings_collection, traffic_data_collection,
    energy_usage_collection, climate_data_collection, alerts_collection,
    logs_collection
)
from app.db.cassandra import session
from app.db.dgraph import client
from datetime import datetime, timedelta
import random
import uuid
import pydgraph

router = APIRouter()

def run_dgraph_mutation(data: dict):
    txn = client.txn()
    try:
        res = txn.mutate(set_obj=data)
        txn.commit()
        return res.uids
    finally:
        txn.discard()

@router.post("/demo/populate")
def populate_all():
    now = datetime.utcnow()

    # MongoDB Inserts
    for i in range(30):
        user_id = users_collection.insert_one({
            "name": f"User {i}",
            "email": f"user{i}@mail.com",
            "role": "admin" if i % 2 == 0 else "operator",
            "created_at": now
        }).inserted_id

        building_id = buildings_collection.insert_one({
            "name": f"Building {i}",
            "type": "Residential" if i % 2 == 0 else "Commercial",
            "location": {"lat": 20.5 + i, "lon": -103.3 - i},
            "zone": f"Zone {i % 5}"
        }).inserted_id

        road_id = roads_collection.insert_one({
            "name": f"Road {i}",
            "type": "Street",
            "coordinates": [{"lat": 20.5 + i, "lon": -103.3 - i}],
            "connected_buildings": [building_id]
        }).inserted_id

        sensor_id = sensors_collection.insert_one({
            "type": "climate" if i % 2 == 0 else "traffic",
            "status": "active",
            "location": {"lat": 20.5 + i, "lon": -103.3 - i},
            "zone": f"Zone {i % 5}",
            "building_id": building_id,
            "power_node_id": f"PN-{i}"
        }).inserted_id

        sensor_readings_collection.insert_one({
            "sensor_id": sensor_id,
            "timestamp": now,
            "type": "temperature",
            "value": str(20 + i)
        })

        traffic_data_collection.insert_one({
            "road_id": road_id,
            "timestamp": now,
            "vehicle_count": 10 + i,
            "avg_speed": 40 + i
        })

        energy_usage_collection.insert_one({
            "building_id": building_id,
            "timestamp": now,
            "consumption_kwh": 100 + i
        })

        climate_data_collection.insert_one({
            "zone": f"Zone {i % 5}",
            "timestamp": now,
            "temperature": 22 + i,
            "humidity": 40 + i,
            "air_quality": 90 - i
        })

        alerts_collection.insert_one({
            "type": "energy",
            "timestamp": now,
            "sensor_id": sensor_id,
            "severity": "high",
            "message": "Overconsumption detected"
        })

        logs_collection.insert_one({
            "user_id": user_id,
            "action": "Created something",
            "timestamp": now,
            "description": "Auto-generated log"
        })

    # Cassandra Inserts
    for i in range(30):
        ts = now - timedelta(minutes=i)
        session.execute(f"""
            INSERT INTO sensor_readings (sensor_id, timestamp, type, value)
            VALUES (%s, %s, %s, %s)
        """, (f"S{i}", ts, "temperature", str(20 + i)))

        session.execute(f"""
            INSERT INTO traffic_data (road_id, timestamp, vehicle_count, avg_speed)
            VALUES (%s, %s, %s, %s)
        """, (f"R{i}", ts, 10 + i, 40 + i))

        session.execute(f"""
            INSERT INTO energy_usage (building_id, timestamp, consumption_kwh)
            VALUES (%s, %s, %s)
        """, (f"B{i}", ts, 100 + i))

        session.execute(f"""
            INSERT INTO climate_data (zone_id, timestamp, temperature, humidity, air_quality)
            VALUES (%s, %s, %s, %s, %s)
        """, (f"Zone {i % 5}", ts, 22 + i, 40 + i, 90 - i))

        session.execute(f"""
            INSERT INTO alerts (alert_type, timestamp, sensor_id, severity, message)
            VALUES (%s, %s, %s, %s, %s)
        """, ("energy", ts, f"S{i}", "high", "Threshold exceeded"))

        session.execute(f"""
            INSERT INTO sensor_status (sensor_id, status)
            VALUES (%s, %s)
        """, (f"S{i}", "active"))

        session.execute(f"""
            INSERT INTO user_activity_log (user_id, timestamp, action, description)
            VALUES (%s, %s, %s, %s)
        """, (f"U{i}", ts, "AutoLog", "Simulated user action"))

    # Dgraph Inserts
    for i in range(30):
        run_dgraph_mutation({
            "dgraph.type": "User",
            "name": f"User D{i}",
            "email": f"user_d{i}@mail.com",
            "role": "viewer",
            "performed": [{
                "dgraph.type": "Log",
                "action": "insert_demo",
                "timestamp": now.isoformat(),
                "description": "Bulk insert example"
            }]
        })

        uid_power = run_dgraph_mutation({
            "dgraph.type": "PowerNode",
            "type": "transformer",
            "status": "online",
            "zone": f"Zone {i % 3}"
        })

        uid_building = run_dgraph_mutation({
            "dgraph.type": "Building",
            "name": f"Building D{i}",
            "type": "Office",
            "location_lat": 20.5 + i,
            "location_lon": -103.3 - i,
            "zone": f"Zone {i % 5}"
        })

        uid_sensor = run_dgraph_mutation({
            "dgraph.type": "Sensor",
            "type": "climate",
            "status": "active",
            "location_lat": 20.5 + i,
            "location_lon": -103.3 - i,
            "zone": f"Zone {i % 5}",
            "installedIn": {"uid": list(uid_building.values())[0]},
            "poweredBy": {"uid": list(uid_power.values())[0]}
        })

        run_dgraph_mutation({
            "dgraph.type": "SensorReading",
            "value": str(25 + i),
            "type": "temperature",
            "timestamp": now.isoformat(),
            "readingOf": {"uid": list(uid_sensor.values())[0]}
        })

    return {"message": "30 records inserted into MongoDB, Cassandra, and Dgraph"}
