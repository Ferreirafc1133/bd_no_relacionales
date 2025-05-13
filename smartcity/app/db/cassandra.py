from cassandra.cluster import Cluster

KEYSPACE = "smartcity"

cluster = Cluster(["127.0.0.1"])
session = cluster.connect()

# Crear keyspace si no existe
session.execute(f"""
    CREATE KEYSPACE IF NOT EXISTS {KEYSPACE}
    WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': '1' }}
""")

# Usar el keyspace
session.set_keyspace(KEYSPACE)

# Crear todas las tablas necesarias
session.execute("""
    CREATE TABLE IF NOT EXISTS sensor_readings (
        sensor_id text,
        timestamp timestamp,
        type text,
        value text,
        PRIMARY KEY (sensor_id, timestamp)
    )
""")
session.execute("""
    CREATE TABLE IF NOT EXISTS traffic_data (
        road_id text,
        timestamp timestamp,
        vehicle_count int,
        avg_speed float,
        PRIMARY KEY (road_id, timestamp)
    )
""")
session.execute("""
    CREATE TABLE IF NOT EXISTS energy_usage (
        building_id text,
        timestamp timestamp,
        consumption_kwh float,
        PRIMARY KEY (building_id, timestamp)
    )
""")
session.execute("""
    CREATE TABLE IF NOT EXISTS climate_data (
        zone_id text,
        timestamp timestamp,
        temperature float,
        humidity float,
        air_quality float,
        PRIMARY KEY (zone_id, timestamp)
    )
""")
session.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        alert_type text,
        timestamp timestamp,
        sensor_id text,
        severity text,
        message text,
        PRIMARY KEY (alert_type, timestamp)
    )
""")
session.execute("""
    CREATE TABLE IF NOT EXISTS sensor_status (
        sensor_id text PRIMARY KEY,
        status text
    )
""")
session.execute("""
    CREATE TABLE IF NOT EXISTS user_activity_log (
        user_id text,
        timestamp timestamp,
        action text,
        description text,
        PRIMARY KEY (user_id, timestamp)
    )
""")
