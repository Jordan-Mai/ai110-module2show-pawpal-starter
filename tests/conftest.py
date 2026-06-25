import os
import sys
from pathlib import Path

# Add the repository root to sys.path so tests can import pawpal_system directly.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
