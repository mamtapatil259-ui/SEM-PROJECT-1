#!/usr/bin/env python3
"""
Auto DataDash - Root Runner
Runs the Python Backend and serves the HTML/CSS/JS frontend.
Run:
    python3 server.py
"""

import sys
import os

# Add backend directory to module search path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from server import run

if __name__ == "__main__":
    run()
