import psutil , socket , time , requests , yaml , json
from flask import Flask, jsonify
from pymongo import MongoClient
import threading , datetime
from fastapi import FastAPI, Request
from pydantic import BaseModel


# Load configuration from config.yaml
def load_config():
    with open("config.yaml", "r") as load:
        config = yaml.safe_load(load)
    return config

# To check system usage and return metrics with status
def get_system_metrics(config):

    # Collect system metrics
    metrics = {
        "timestamp": time.time(),
        "hostname": socket.gethostname(),
        "cpu_percent": psutil.cpu_percent(percpu=True),
        "cpu_total_percent": psutil.cpu_percent(),
        "memory": dict(psutil.virtual_memory()._asdict()),
        "disk": {part.mountpoint: dict(psutil.disk_usage(part.mountpoint)._asdict())
                 for part in psutil.disk_partitions() if part.fstype}
    }

    # Check for CPU usage against the thresholds
    cpu_percent = metrics["cpu_total_percent"]
    cpu_status = ""
    if cpu_percent >= config['thresholds']['cpu'][2]:
        cpu_status = f"Critical: {cpu_percent}%"
    elif cpu_percent >= config['thresholds']['cpu'][1]:
        cpu_status = f"High: {cpu_percent}%"
    elif cpu_percent >= config['thresholds']['cpu'][0]:
        cpu_status = f"Moderate: {cpu_percent}%"
    else:
        cpu_status = f"Normal: {cpu_percent}%"

    # Check for Memory usage against the thresholds
    memory_percent = metrics["memory"]["percent"]
    memory_status = ""
    if memory_percent >= config['thresholds']['memory'][2]:
        memory_status = f"Critical: {memory_percent}%"
    elif memory_percent >= config['thresholds']['memory'][1]:
        memory_status = f"High: {memory_percent}%"
    elif memory_percent >= config['thresholds']['memory'][0]:
        memory_status = f"Moderate: {memory_percent}%"
    else:
        memory_status = f"Normal: {memory_percent}%"

    # Check for Disk usage against the thresholds
    disk_percent = metrics["disk"]['/']['percent']  # assuming checking root partition
    disk_status = ""  
    if disk_percent >= config['thresholds']['disk'][2]:
        disk_status = f"Critical: {disk_percent}%"
    elif disk_percent >= config['thresholds']['disk'][1]:
        disk_status = f"High: {disk_percent}%"
    elif disk_percent >= config['thresholds']['disk'][0]:
        disk_status = f"Moderate: {disk_percent}%"
    else:
        disk_status = f"Normal: {disk_percent}%"

    print(metrics["disk"].keys())

    # Update the metrics dictionary with the status of each resource
    metrics.update({
        "cpu_status": cpu_status,
        "memory_status": memory_status,
        "disk_status": disk_status
    })

    return metrics


# config = load_config()
# metrics = get_system_metrics(config)
# print(json.dumps(metrics, indent=0))



# Function to send metrics to the cloud endpoint
def send_to_cloud(config, metrics):
    try:
        response = requests.post(config['cloud_endpoint'], json=metrics)
        if response.status_code == 200:
            print("Metrics successfully sent to cloud.")
        else:
            print(f"Failed to send metrics to cloud. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending metrics to cloud: {e}")






