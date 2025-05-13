from fastapi import APIRouter
from app.db.mongo import users_collection, buildings_collection, sensors_collection
from app.db.cassandra import session
from app.db.dgraph import client
from fastapi.encoders import jsonable_encoder

router = APIRouter()

def clean_mongo(doc):
    return {k: str(v) if str(type(v)) == "<class 'bson.objectid.ObjectId'>" else v for k, v in doc.items()}

def query_dgraph(query):
    txn = client.txn(read_only=True)
    try:
        res = txn.query(query)
        return res.json
    finally:
        txn.discard()

@router.get("/demo/overview")
def get_overview():
    mongo_users = [clean_mongo(u) for u in users_collection.find().limit(5)]
    mongo_buildings = [clean_mongo(b) for b in buildings_collection.find().limit(5)]
    mongo_sensors = [clean_mongo(s) for s in sensors_collection.find().limit(5)]

    cassandra_sensors = session.execute("SELECT * FROM sensor_readings LIMIT 5")
    cassandra_traffic = session.execute("SELECT * FROM traffic_data LIMIT 5")
    cassandra_energy = session.execute("SELECT * FROM energy_usage LIMIT 5")

    dgraph_users = query_dgraph("""
    {
      users(func: type(User), first: 5) {
        uid
        name
        email
        role
      }
    }""")

    dgraph_buildings = query_dgraph("""
    {
      buildings(func: type(Building), first: 5) {
        uid
        name
        type
        location_lat
        location_lon
        zone
      }
    }""")

    return jsonable_encoder({
        "mongo": {
            "users": mongo_users,
            "buildings": mongo_buildings,
            "sensors": mongo_sensors
        },
        "cassandra": {
            "sensor_readings": [dict(r._asdict()) for r in cassandra_sensors],
            "traffic_data": [dict(r._asdict()) for r in cassandra_traffic],
            "energy_usage": [dict(r._asdict()) for r in cassandra_energy]
        },
        "dgraph": {
            "users": dgraph_users,
            "buildings": dgraph_buildings
        }
    })
