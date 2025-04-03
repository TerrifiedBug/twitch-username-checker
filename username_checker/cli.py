"""CLI entry point for the username checker."""

from username_checker.config.loader import get_targets_from_env, load_config
from username_checker.services.checker import check_username_availability
from username_checker.services.notification import send_notifications


def main():
    """Main entry point for the CLI."""
    config = load_config()
    screenshot_conf = config.get("screenshots", {})
    usernames, websites = get_targets_from_env()

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
