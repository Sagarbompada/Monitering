import requests
import yaml
from metrics import load_config, get_system_metrics

# Load Slack webhook from config

config = load_config()

SLACK_WEBHOOK = config.get("slack_webhook")

def send_slack_alert(message):
    if not SLACK_WEBHOOK:
        print("Slack webhook not set in config.")
        return

    payload = {
        "text": f":rotating_light: ALERT: {message}"
    }

    response = requests.post(SLACK_WEBHOOK, json=payload)
    if response.status_code != 200:
        print(f"Failed to send Slack alert: {response.status_code}, {response.text}")
