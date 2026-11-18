from dataclasses import dataclass
from typing import Iterable
import cv2
import numpy as np

@dataclass
class ZoneResult:
    inside: bool
    normalized_centroid: tuple[float, float]

def parse_zone(text: str):
    """Parse `x,y; x,y; ...` normalized points and validate a polygon."""
    points = []
    for pair in text.split(";"):
        x, y = map(float, pair.strip().split(",")); points.append((x, y))
    if len(points) < 3 or any(not (0 <= x <= 1 and 0 <= y <= 1) for x,y in points):
        raise ValueError("Zone needs at least three normalized x,y points in the range 0–1.")
    return points

def contains(bbox, zone, width, height) -> ZoneResult:
    x1,y1,x2,y2 = bbox; cx, cy = (x1+x2)/2, (y1+y2)/2
    polygon = np.array([(int(x*width), int(y*height)) for x,y in zone], dtype=np.int32)
    return ZoneResult(cv2.pointPolygonTest(polygon, (float(cx), float(cy)), False) >= 0, (cx/width, cy/height))

def draw_zone(frame, zone, color=(0, 215, 255)):
    h,w = frame.shape[:2]; pts = np.array([(int(x*w),int(y*h)) for x,y in zone], np.int32)
    overlay = frame.copy(); cv2.fillPoly(overlay, [pts], color); cv2.addWeighted(overlay,.14,frame,.86,0,frame)
    cv2.polylines(frame,[pts],True,color,2); cv2.putText(frame,"DANGER ZONE",tuple(pts[0]),cv2.FONT_HERSHEY_SIMPLEX,.6,color,2)
    return frame
