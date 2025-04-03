"""Multi-site username checker using environment-based config."""

import json
import os

import requests
from dotenv import load_dotenv
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError, sync_playwright

load_dotenv()


def load_config():
    """Load config json relative to the script location."""
    with open("/app/config.json", "r", encoding="utf-8") as f:
        return json.load(f)


def send_discord_notification(webhook_url, message):
    """Send a message to a Discord webhook."""
    try:
        requests.post(webhook_url, json={"content": message}, timeout=10)
        print("[🔔] Discord notification sent.")
    except requests.RequestException as error:
        print(f"[!] Discord notification failed: {error}")


def send_callmebot_sms(phone_number, api_key, message):
    """Send a message via CallMeBot."""
    try:
        url = (
            f"https://api.callmebot.com/whatsapp.php?"
            f"phone={phone_number}&apikey={api_key}&text={requests.utils.quote(message)}"
        )
        requests.get(url, timeout=10)
        print("[📱] CallMeBot notification sent.")
    except requests.RequestException as error:
        print(f"[!] CallMeBot notification failed: {error}")


def send_notifications(message):
    """Send notifications based on environment config."""
    if os.getenv("DISCORD_ENABLED", "false").lower() == "true":
        send_discord_notification(os.getenv("DISCORD_WEBHOOK"), message)
    if os.getenv("CALLMEBOT_ENABLED", "false").lower() == "true":
        send_callmebot_sms(
            os.getenv("CALLMEBOT_PHONE"),
            os.getenv("CALLMEBOT_APIKEY"),
            message,
        )


def check_username_availability(username, site_conf, screenshot_conf, site_name):
    """Check if a username is available on a specific site."""
    print(f"\n[*] Checking {site_name} username: {username}")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        if site_conf["type"] == "direct":
            url = f"{site_conf['url']}{username}"
            error_selector = site_conf.get("error_selector")

            if not error_selector:
                print(
                    f"[!] Missing 'error_selector' in config.json for site '{site_name}'"
                )
                return None, False

            page.goto(url)
            try:
                page.wait_for_selector(error_selector, timeout=1500)
                is_available = (
                    True  # Error message present = user not found = available
                )
                result_text = "Available"
            except TimeoutError:
                is_available = False  # Error message not found = user exists
                result_text = "Taken"

        elif site_conf["type"] == "form":
            page.goto(site_conf["url"])

            # Required selectors from config
            username_field = site_conf.get("username_field")
            submit_button = site_conf.get("submit_button")
            result_selector = site_conf.get("result_selector")
            success_class = site_conf.get("success_class")
            success_text = site_conf.get("success_text")

            if not all([username_field, submit_button, result_selector]):
                print(
                    f"[!] Missing one or more required form keys in config for site '{site_name}'"
                )
                return None, False

            try:
                page.fill(username_field, username)
                page.click(submit_button)
                page.wait_for_selector(result_selector, timeout=1500)

                result_elem = page.query_selector(result_selector)
                if not result_elem:
                    print("[!] No result element found.")
                    return None, False

                result_text = result_elem.inner_text().strip()
                result_classes = result_elem.get_attribute("class") or ""

                is_available = False
                if success_class and success_class in result_classes:
                    is_available = True
                if success_text and success_text.lower() in result_text.lower():
                    is_available = True

            except (TimeoutError, AttributeError, PlaywrightError) as error:
                print(f"[!] Error while checking username on {site_name}: {error}")
                result_text = None
                is_available = False

        else:
            print(
                f"[!] Unknown check type '{site_conf['type']}' for site '{site_name}'"
            )
            return None, False

        # Screenshot support
        screenshot_enabled = (
            os.getenv(
                "SCREENSHOTS_ENABLED", str(screenshot_conf.get("enabled", False))
            ).lower()
            == "true"
        )

        if screenshot_enabled:
            screenshot_path = screenshot_conf["path_format"].format(
                site=site_name, username=username
            )
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"[*] Screenshot saved: {screenshot_path}")

        browser.close()
        return result_text, is_available


def main():
    """Main entry point."""
    config = load_config()
    screenshot_conf = config.get("screenshots", {})

    usernames_raw = os.getenv("USERNAMES", "")
    websites_raw = os.getenv("WEBSITES", "")

    usernames = [u.strip() for u in usernames_raw.split(",") if u.strip()]
    websites = [w.strip() for w in websites_raw.split(",") if w.strip()]

    if not usernames:
        print("[!] No usernames provided via environment.")
        return

    if not websites:
        print("[!] No websites provided via environment.")
        return

    for username in usernames:
        for site_name in websites:
            site_conf = config.get(site_name)
            if not site_conf:
                print(f"[!] Site '{site_name}' not found in config.json.")
                continue

            result_text, is_available = check_username_availability(
                username, site_conf, screenshot_conf, site_name
            )

            if result_text:
                print(f"[✔️] {site_name}/{username}: {result_text}")
                if is_available:
                    message = f'Username "{username}" is available on {site_name}.'
                    send_notifications(message)
            else:
                print(f"[❌] {site_name}/{username}: No result found.")


if __name__ == "__main__":
    main()
