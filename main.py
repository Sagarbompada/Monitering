# main.py

import time
import logging
from metrics import get_system_metrics, load_config, send_to_cloud
from Monitering.alert import send_slack_alert
from pymongo import MongoClient

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Load config
config = load_config()

# Setup MongoDB (optional)
try:
    mongo_enabled = True
    client = MongoClient("mongodb://localhost:27017/")
    db = client["system_metrics"]
    collection = db["metrics"]
    logging.info("Connected to MongoDB")
except Exception as e:
    mongo_enabled = False
    logging.warning(f"MongoDB not available: {e}")

# Main loop
if __name__ == "__main__":
    interval = config.get("interval", 60)  # default to 60 seconds

    while True:
        metrics = get_system_metrics(config)
        logging.info(f"Collected Metrics: {metrics}")

        # Save to MongoDB
        if mongo_enabled:
            collection.insert_one(metrics)
            logging.info("Metrics saved to MongoDB")

        # Send to cloud endpoint
        send_to_cloud(config, metrics)

        # Send Slack alert on threshold breach
        if "Critical" in metrics["cpu_status"] or "Critical" in metrics["memory_status"]:
            message = f"CPU: {metrics['cpu_status']}, Memory: {metrics['memory_status']}"
            send_slack_alert(message)

        time.sleep(interval)
