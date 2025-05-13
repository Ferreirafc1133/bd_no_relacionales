import grpc
import pydgraph

client_stub = pydgraph.DgraphClientStub('localhost:9080')
client = pydgraph.DgraphClient(client_stub)

def set_schema():
    schema = """
    name: string @index(term) .
    type: string @index(term) .
    email: string @index(term) .
    role: string @index(exact) .
    location_lat: float .
    location_lon: float .
    zone: string @index(exact) .
    temperature: float .
    humidity: float .
    air_quality: float .
    status: string @index(exact) .
    timestamp: datetime .
    value: string .
    action: string @index(term) .
    description: string .
    coordinates: string .
    lastReading: datetime .
    connectedToBuilding: uid .

    hasSensor: [uid] .
    connectedToRoad: [uid] .
    installedIn: uid .
    monitors: uid .
    poweredBy: uid .
    feeds: [uid] .
    performed: [uid] .
    readingOf: uid .

    type User {
        name
        email
        role
        performed
    }

    type Log {
        action
        timestamp
        description
    }

    type Building {
        name
        type
        location_lat
        location_lon
        zone
        hasSensor
        connectedToRoad
    }

    type Road {
        name
        type
        coordinates
        connectedToBuilding
    }

    type Sensor {
        type
        status
        location_lat
        location_lon
        lastReading
        zone
        installedIn
        monitors
        poweredBy
    }

    type SensorReading {
        value
        type
        timestamp
        readingOf
    }

    type PowerNode {
        type
        status
        zone
        feeds
    }
    """
    op = pydgraph.Operation(schema=schema)
    client.alter(op)

set_schema()
