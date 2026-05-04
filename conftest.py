# conftest.py
# Ensure tests can import project packages located in the `src/` directory.
# Place this file at the repository root (same directory that contains `src/`).
#
# This file:
# - Prepends the project's `src/` directory to sys.path so pytest can import packages like `core`.
# - Sets a sensible default for DJANGO_SETTINGS_MODULE if it isn't already set.
#
# Notes:
# - We avoid importing Django here; pytest-django will initialize Django when it's ready.
# - If you prefer not to modify environment variables here, remove the os.environ.setdefault line.

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / "src"

if str(SRC_DIR) not in sys.path:
    # Insert at position 0 so the project packages are preferred over system/site packages.
    if SRC_DIR.exists():
        sys.path.insert(0, str(SRC_DIR))
    else:
        # If src/ does not exist, still try to be helpful by adding the repo root.
        # This handles cases where the project layout differs.
        sys.path.insert(0, str(ROOT))

# Provide a reasonable default settings module for pytest-django.
# Adjust this if your Django settings module path differs.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.dev")
