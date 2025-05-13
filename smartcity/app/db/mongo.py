# db/mongo.py
from pymongo import MongoClient

# mongo.py
client = MongoClient("mongodb://localhost:27017")
db = client["smartcity"]

# Colecciones
users_collection = db["users"]
buildings_collection = db["buildings"]
logs_collection = db["logs"]
roads_collection = db["roads"]
sensors_collection = db["sensors"]
sensor_readings_collection = db["sensor_readings"]
traffic_data_collection = db["traffic_data"]
energy_usage_collection = db["energy_usage"]
climate_data_collection = db["climate_data"]
alerts_collection = db["alerts"]
logs_collection = db["logs"]
