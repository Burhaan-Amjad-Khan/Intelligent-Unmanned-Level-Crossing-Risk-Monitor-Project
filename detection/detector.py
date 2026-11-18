"""Genuine Ultralytics YOLO inference; no generated or simulated detections."""
from dataclasses import dataclass
from typing import List
import numpy as np
from config.settings import MODEL_NAME, SUPPORTED_CLASSES

@dataclass
class Detection:
    label: str
    confidence: float
    bbox: tuple[int, int, int, int]
    source: str = "REAL_YOLO"

class YOLODetector:
    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self.model = None
        self.error = None

    def load(self) -> bool:
        try:
            from ultralytics import YOLO
            self.model = YOLO(self.model_name)
            self.error = None
            return True
        except Exception as exc:
            self.error = (f"Unable to load {self.model_name}: {exc}. Install ultralytics and allow "
                          "the first-run model download, or place model weights where Ultralytics can find them.")
            return False

    def detect(self, frame: np.ndarray, confidence: float) -> List[Detection]:
        if self.model is None and not self.load():
            return []
        try:
            result = self.model(frame, conf=confidence, verbose=False)[0]
            names = result.names
            items = []
            for box in result.boxes:
                label = str(names[int(box.cls[0])])
                if label not in SUPPORTED_CLASSES:
                    continue
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                items.append(Detection(label, float(box.conf[0]), (x1, y1, x2, y2)))
            return items
        except Exception as exc:
            self.error = f"YOLO inference failed: {exc}"
            return []
