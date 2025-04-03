"""Configuration module for username checker."""

from username_checker.config.loader import (
    get_screenshot_config,
    get_targets_from_env,
    load_config,
)

__all__ = ["load_config", "get_targets_from_env", "get_screenshot_config"]
