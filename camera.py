

import cv2


class Camera:
    def __init__(self, source=0, width=720, height=720, flip=True):
       
        self.source = source
        self.flip = flip
        self.cap = cv2.VideoCapture(source)

        if not self.cap.isOpened():
            raise RuntimeError(f"Could not open camera/source: {source}")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def read(self):
        
        success, frame = self.cap.read()
        if not success:
            return False, None
        if self.flip:
            frame = cv2.flip(frame, 1)
        return True, frame

    def get_fps(self):
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        return fps if fps > 0 else 30.0

    def release(self):
        self.cap.release()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()