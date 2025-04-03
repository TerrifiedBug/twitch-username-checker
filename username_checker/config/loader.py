"""Configuration loading utilities."""

import json
import os
from typing import Dict, List, Tuple


def load_config(config_path: str = "/app/config.json") -> Dict:
    """Load config json relative to the script location."""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"[!] Error loading config: {error}")
        return {}


def get_targets_from_env() -> Tuple[List[str], List[str]]:
    """Get usernames and websites to check from environment variables."""
    usernames_raw = os.getenv("USERNAMES", "")
    websites_raw = os.getenv("WEBSITES", "")

    usernames = [u.strip() for u in usernames_raw.split(",") if u.strip()]
    websites = [w.strip() for w in websites_raw.split(",") if w.strip()]

    return usernames, websites


def get_screenshot_config(screenshot_conf: Dict) -> bool:
    """Get screenshot configuration from environment and config."""
    return (
        os.getenv(
            "SCREENSHOTS_ENABLED", str(screenshot_conf.get("enabled", False))
        ).lower()
        == "true"
    )
