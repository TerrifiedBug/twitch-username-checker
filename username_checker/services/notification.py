"""Notification services for username checker."""

import os

import requests


def send_discord_notification(webhook_url: str, message: str) -> bool:
    """Send a message to a Discord webhook.

    Args:
        webhook_url: The Discord webhook URL
        message: The message to send

    Returns:
        bool: True if notification was sent successfully
    """
    try:
        response = requests.post(webhook_url, json={"content": message}, timeout=10)
        response.raise_for_status()
        print("[🔔] Discord notification sent.")
        return True
    except requests.RequestException as error:
        print(f"[!] Discord notification failed: {error}")
        return False


def send_callmebot_sms(phone_number: str, api_key: str, message: str) -> bool:
    """Send a message via CallMeBot.

    Args:
        phone_number: The phone number to send to
        api_key: CallMeBot API key
        message: The message to send

    Returns:
        bool: True if notification was sent successfully
    """
    try:
        url = (
            f"https://api.callmebot.com/whatsapp.php?"
            f"phone={phone_number}&apikey={api_key}&text={requests.utils.quote(message)}"
        )
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print("[📱] CallMeBot notification sent.")
        return True
    except requests.RequestException as error:
        print(f"[!] CallMeBot notification failed: {error}")
        return False


def send_notifications(message: str) -> None:
    """Send notifications based on environment config.

    Args:
        message: The message to send through configured notification channels
    """
    # Discord notifications
    if os.getenv("DISCORD_ENABLED", "false").lower() == "true":
        webhook_url = os.getenv("DISCORD_WEBHOOK")
        if webhook_url:
            send_discord_notification(webhook_url, message)
        else:
            print("[!] Discord enabled but no webhook URL provided.")

    # CallMeBot notifications
    if os.getenv("CALLMEBOT_ENABLED", "false").lower() == "true":
        phone_number = os.getenv("CALLMEBOT_PHONE")
        api_key = os.getenv("CALLMEBOT_APIKEY")

        if phone_number and api_key:
            send_callmebot_sms(phone_number, api_key, message)
        else:
            print("[!] CallMeBot enabled but missing phone number or API key.")
