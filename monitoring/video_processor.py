from datetime import datetime
import cv2
from monitoring.danger_zone import contains, draw_zone

class VideoProcessor:
    def __init__(self, detector, tracker): self.detector, self.tracker = detector, tracker
    def process(self, frame, zone, confidence):
        draw_zone(frame, zone)
        tracked = self.tracker.update(self.detector.detect(frame, confidence))
        records = []
        for item in tracked:
            x1,y1,x2,y2 = item.detection.bbox; result = contains(item.detection.bbox,zone,frame.shape[1],frame.shape[0])
            if result.inside and not item.in_zone: item.entered_zone_at = datetime.now()
            if not result.inside: item.entered_zone_at = None
            item.in_zone = result.inside
            elapsed = (datetime.now()-item.entered_zone_at).total_seconds() if item.entered_zone_at else 0
            color=(0,0,255) if result.inside else (0,220,0)
            cv2.rectangle(frame,(x1,y1),(x2,y2),color,2)
            cv2.putText(frame,f"#{item.track_id} {item.detection.label} {item.detection.confidence:.0%}",(x1,max(20,y1-8)),cv2.FONT_HERSHEY_SIMPLEX,.55,color,2)
            records.append({"id":item.track_id,"label":item.detection.label,"confidence":item.detection.confidence,"bbox":item.detection.bbox,"in_zone":result.inside,"duration":elapsed,"source":"REAL_YOLO"})
        return frame, records
