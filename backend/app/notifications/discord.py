import os

import requests
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def send_discord_notification(title: str, message: str):
    """Sends a simple message to the configured Discord webhook. No-op if not set up yet."""
    if not DISCORD_WEBHOOK_URL:
        return

    payload = {"content": f"**{title}**\n{message}"}
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
    except requests.RequestException as e:
        print(f"Failed to send Discord notification: {e}")
