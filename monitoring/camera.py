import cv2

class VideoSource:
    def __init__(self): self.capture = None; self.description = "Stopped"
    def open(self, source):
        self.release()
        try:
            source = int(source) if isinstance(source, str) and source.isdigit() else source
            self.capture = cv2.VideoCapture(source)
            if not self.capture.isOpened():
                self.release(); self.description = "Unable to open source"; return False
            self.description = f"Active: {source}"; return True
        except Exception as exc:
            self.description = f"Source error: {exc}"; return False
    def read(self):
        if self.capture is None: return False, None
        ok, frame = self.capture.read()
        if not ok: self.description = "End of stream or frame-read error"
        return ok, frame
    def release(self):
        if self.capture is not None: self.capture.release()
        self.capture = None
