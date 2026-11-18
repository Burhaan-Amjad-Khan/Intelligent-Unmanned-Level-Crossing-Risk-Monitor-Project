from dataclasses import dataclass
from datetime import datetime
from typing import Iterable
from detection.detector import Detection

@dataclass
class TrackedObject:
    track_id: int
    detection: Detection
    first_seen: datetime
    last_seen: datetime
    in_zone: bool = False
    entered_zone_at: datetime | None = None

class CentroidTracker:
    """Lightweight IOU tracker suitable for dashboard visualization, not safety certification."""
    def __init__(self, iou_threshold=0.25):
        self.objects: dict[int, TrackedObject] = {}
        self.next_id, self.iou_threshold = 1, iou_threshold

    @staticmethod
    def _iou(a, b):
        ax1, ay1, ax2, ay2 = a; bx1, by1, bx2, by2 = b
        inter = max(0, min(ax2,bx2)-max(ax1,bx1))*max(0, min(ay2,by2)-max(ay1,by1))
        union = (ax2-ax1)*(ay2-ay1)+(bx2-bx1)*(by2-by1)-inter
        return inter / union if union else 0

    def update(self, detections: Iterable[Detection], now=None):
        now = now or datetime.now()
        unmatched = list(self.objects)
        matched = []
        for det in detections:
            candidates = [(self._iou(det.bbox, self.objects[i].detection.bbox), i) for i in unmatched
                          if self.objects[i].detection.label == det.label]
            score, best = max(candidates, default=(0, None))
            if best is not None and score >= self.iou_threshold:
                obj = self.objects[best]; obj.detection = det; obj.last_seen = now; unmatched.remove(best); matched.append(obj)
            else:
                obj = TrackedObject(self.next_id, det, now, now); self.objects[self.next_id] = obj; self.next_id += 1; matched.append(obj)
        self.objects = {i:o for i,o in self.objects.items() if (now-o.last_seen).total_seconds() < 2}
        return matched
