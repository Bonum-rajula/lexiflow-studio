# conftest.py
import sys
from pathlib import Path

# Add the project root to Python path so that 'src' is importable
root_path = Path(__file__).parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))