import asyncio
import nats
import psycopg2
import os
import random
import json
import time
from datetime import datetime

# Config
DB_HOST = os.getenv("DB_HOST", "timescaledb")
DB_URL = f"host={DB_HOST} dbname=postgres user=postgres password=password"
NATS_URL = os.getenv("NATS_URL", "nats://nats-server:4222")
SUBJECT = "factory.sensor.temperature"

async def get_db_connection():
    """Resilient connection helper."""
    while True:
        try:
            return psycopg2.connect(DB_URL)
        except:
            print("NATS App: Waiting for database...")
            await asyncio.sleep(2)

async def message_handler(msg):
    """Consumer logic: Triggered whenever a message hits the subject."""
    try:
        data = json.loads(msg.data.decode())
        val = data.get("value")
        
        conn = await get_db_connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO nats_data (time, subject, value, unit) VALUES (%s, %s, %s, %s)",
                    (datetime.now(), msg.subject, val, data.get("unit"))
                )
        conn.close()
        print(f"[NATS Sub] Ingested {msg.subject}: {val}")
    except Exception as e:
        print(f"Ingestion Error: {e}")

async def main():
    # Connect to NATS
    nc = await nats.connect(NATS_URL)
    print(f"NATS App: Connected to {NATS_URL}")

    # Subscribe to sensor data
    await nc.subscribe(SUBJECT, cb=message_handler)

    # Producer Loop
    while True:
        payload = {
            "value": round(random.uniform(18.0, 26.0), 2),
            "unit": "C"
        }
        await nc.publish(SUBJECT, json.dumps(payload).encode())
        await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(main())