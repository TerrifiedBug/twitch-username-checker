"""Username availability checking service."""

from typing import Dict, Optional, Tuple

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

from username_checker.config.loader import get_screenshot_config


def check_username_availability(
    username: str, site_conf: Dict, screenshot_conf: Dict, site_name: str
) -> Tuple[Optional[str], bool]:
    """Check if a username is available on a specific site.

    Args:
        username: The username to check
        site_conf: The site configuration
        screenshot_conf: Screenshot configuration
        site_name: The name of the site being checked

    Returns:
        Tuple containing result text and availability status
    """
    print(f"\n[*] Checking {site_name} username: {username}")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Determine check type and perform appropriate check
            if site_conf["type"] == "direct":
                result_text, is_available = _check_direct(
                    page, username, site_conf, site_name
                )
            elif site_conf["type"] == "form":
                result_text, is_available = _check_form(
                    page, username, site_conf, site_name
                )
            else:
                print(
                    f"[!] Unknown check type '{site_conf['type']}' for site '{site_name}'"
                )
                return None, False

            # Handle screenshots if enabled
            screenshot_enabled = get_screenshot_config(screenshot_conf)
            if screenshot_enabled and "path_format" in screenshot_conf:
                screenshot_path = screenshot_conf["path_format"].format(
                    site=site_name, username=username
                )
                page.screenshot(path=screenshot_path, full_page=True)
                print(f"[*] Screenshot saved: {screenshot_path}")

            return result_text, is_available

        except Exception as e:
            print(f"[!] Unexpected error during check: {e}")
            return None, False
        finally:
            browser.close()


def _check_direct(
    page, username: str, site_conf: Dict, site_name: str
) -> Tuple[Optional[str], bool]:
    """Check username using direct URL approach.

    Args:
        page: Playwright page object
        username: The username to check
        site_conf: The site configuration
        site_name: The name of the site

    Returns:
        Tuple containing result text and availability status
    """
    url = f"{site_conf['url']}{username}"
    error_selector = site_conf.get("error_selector")

    if not error_selector:
        print(f"[!] Missing 'error_selector' in config.json for site '{site_name}'")
        return None, False

    page.goto(url)
    try:
        page.wait_for_selector(error_selector, timeout=1500)
        # Error message present = user not found = available
        return "Available", True
    except PlaywrightTimeoutError:
        # Error message not found = user exists
        return "Taken", False


def _check_form(
    page, username: str, site_conf: Dict, site_name: str
) -> Tuple[Optional[str], bool]:
    """Check username using form submission approach.

    Args:
        page: Playwright page object
        username: The username to check
        site_conf: The site configuration
        site_name: The name of the site

    Returns:
        Tuple containing result text and availability status
    """
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
        page.goto(site_conf["url"])
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

        return result_text, is_available

    except (PlaywrightTimeoutError, AttributeError, PlaywrightError) as error:
        print(f"[!] Error while checking username on {site_name}: {error}")
        return None, False
