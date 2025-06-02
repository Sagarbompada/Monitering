from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import logging
import os
from pymongo import MongoClient
from metrics import get_system_metrics, load_config

app = FastAPI()
buffer = []

# Allow cross-origin requests for testing/dashboard if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient("mongodb://localhost:27017/")
db = client["system_metrics"]
collection = db["metrics"]

# Ensure log directory exists
os.makedirs("logs", exist_ok=True)

# Setup logging
logging.basicConfig(
    filename="logs/ingestion.log",
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
)


@app.post("/ingest")
async def ingest(payload: Request):
    data = await payload.json()
    buffer.append(data)

    collection.insert_one(data)    # MongoDB data collection

    # Log to file
    logging.info(json.dumps(data))

    # Print to stdout (for debugging)
    print(f"Received metric: {json.dumps(data)}")

    return {"status": "received"}


@app.get("/buffer")
def get_buffer():
    return buffer[-10:]  # Return last 10 records
