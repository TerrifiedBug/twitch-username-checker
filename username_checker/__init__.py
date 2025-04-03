"""Username checker package."""

__version__ = "1.0.0"

# Make core modules available at package level
from username_checker.config import loader
from username_checker.services import checker, notification

__all__ = ["loader", "checker", "notification"]
