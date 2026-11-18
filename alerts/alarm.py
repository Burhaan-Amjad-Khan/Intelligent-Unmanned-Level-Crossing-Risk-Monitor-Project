import time
import threading

class Alarm:
    def __init__(self): self.muted=False; self.last={}; self.error=None
    def beep(self, key, cooldown=12):
        if self.muted or time.time()-self.last.get(key,0)<cooldown: return False
        self.last[key]=time.time()
        try:
            # Native Windows tone is dependable and requires no media asset.
            import winsound
            threading.Thread(target=lambda: winsound.Beep(1100, 350), daemon=True).start()
            self.error=None; return True
        except Exception as windows_exc:
            try:
                import pygame
                if not pygame.mixer.get_init(): pygame.mixer.init()
                pygame.mixer.Sound(buffer=b"\x00\x00" * 2205).play()
                return True
            except Exception as exc:
                self.error=f"Audio unavailable (Windows: {windows_exc}; fallback: {exc})"; return False
