
import time
import logging
from metrics import get_system_metrics, load_config
from alert import send_slack_alert
from pymongo import MongoClient
from metrics import get_system_metrics, load_config, send_to_cloud, send_to_influxdb

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Load config
config = load_config()

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["system_metrics"]
collection = db["metrics"]

# Main loop
if __name__ == "__main__":
    interval = config.get("interval")  # default to 60 seconds

    while True:
        metrics = get_system_metrics(config) 
        logging.info(f"Collected Metrics: {metrics}")          # Logging
        send_to_influxdb(metrics, config)                    #send metrics to influx db

        # Save to MongoDB
        collection.insert_one(metrics)
        logging.info("Metrics saved to MongoDB")

        # Send to cloud endpoint
        # send_to_cloud(config, metrics)

        # Send Slack alert on threshold breach
        if "Critical" in metrics["cpu_status"] or "Critical" in metrics["memory_status"]:
            message = f"CPU: {metrics['cpu_status']}, Memory: {metrics['memory_status']}"
            send_slack_alert(message)

        time.sleep(interval)
