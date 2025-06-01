# Monitering
Python-based system resource monitoring service using Flask, FastAPI , MongoDB, and Slack alerts.

Metrics.py -- Collects CPU, Memory and Disk Space metrics
app.py     -- Rest API for metrics collection and MongoDB persistance
alert.py   -- Sends Slack Alerts
ingestion.py -- Accepts external metric payloads
unittest.py  -- Checks and Units tests the code
Dockerfile   -- TO dockerize the process
Config.yaml  -- Contains the Threshholds and static data


