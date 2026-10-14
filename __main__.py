import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from snake import ui

from snake.main import run

run()
