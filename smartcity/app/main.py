# main.py
from fastapi import FastAPI
from app.routes import users, buildings, roads, sensors, sensor_readings, traffic, energy, climate, alerts, logs, c_sensor_readings, c_data, dgraph_data, demo, overview, mongo_demo

app = FastAPI()
app.include_router(users.router)
app.include_router(buildings.router)
app.include_router(roads.router)
app.include_router(sensors.router)
app.include_router(sensor_readings.router)
app.include_router(traffic.router)
app.include_router(energy.router)
app.include_router(climate.router)
app.include_router(alerts.router)
app.include_router(logs.router)
app.include_router(c_sensor_readings.router)
app.include_router(c_data.router)
app.include_router(dgraph_data.router)
app.include_router(demo.router)
app.include_router(overview.router)
app.include_router(mongo_demo.router)