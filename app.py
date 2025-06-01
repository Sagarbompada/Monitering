from flask import Flask, jsonify
from pymongo import MongoClient
from Monitering.alert import send_slack_alert
from metrics import load_config, get_system_metrics
import datetime


# Flask setup
app = Flask(__name__)
config = load_config()
metrics = get_system_metrics(config)  # to get metrics


# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["system_metrics"]
collection = db["metrics"]

# Flask route
@app.route("/metrics", methods=["GET"])
def get_metrics():
    metrics = get_system_metrics(config)   #to get metrics
    collection.insert_one({
        **metrics,
        "timestamp": datetime.datetime.utcnow()

        })

if __name__ == "__main__":
   # start_background_monitor()
    app.run(debug=True)

send_slack_alert(f"CPU Status: {metrics['cpu_status']}, Memory Status: {metrics['memory_status']}")
