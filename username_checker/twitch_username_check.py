#!/usr/bin/env python3
"""
Main entry point for the Docker container.
This script maintains the original interface for compatibility with docker-entrypoint.sh.
"""

from dotenv import load_dotenv
from username_checker.cli import main

if __name__ == "__main__":
    load_dotenv()
    main()
