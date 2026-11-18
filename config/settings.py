from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATABASE_PATH = DATA_DIR / "crossing_monitor.db"
MODEL_NAME = "yolo11n.pt"  # Ultralytics downloads this genuine pretrained weight on first use.
SUPPORTED_CLASSES = {"person", "bicycle", "car", "motorcycle", "bus", "truck", "train"}
DEFAULT_CONFIDENCE = 0.45
DEFAULT_ZONE = [(0.28, 0.42), (0.72, 0.42), (0.88, 0.92), (0.12, 0.92)]
ALERT_COOLDOWN_SECONDS = 12
APP_TITLE = "Intelligent Unmanned Level-Crossing Risk Monitor"
PROJECT_ID = "ISET_IP - 028"
