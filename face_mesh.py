

import os
import time
import urllib.request

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import (
    FaceLandmarker,
    FaceLandmarkerOptions,
    RunningMode,
)

# --- Landmark index groups (same numbering as legacy FaceMesh w/ refine_landmarks=True) ---

LEFT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
RIGHT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]

LEFT_EYE_CORNERS = (33, 133)     # outer, inner
RIGHT_EYE_CORNERS = (362, 263)   # inner, outer
LEFT_EYE_LIDS = (159, 145)       # top, bottom
RIGHT_EYE_LIDS = (386, 374)      # top, bottom

LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]

_MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/face_landmarker/"
    "face_landmarker/float16/1/face_landmarker.task"
)
_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "face_landmarker.task")


def _ensure_model():
    if os.path.exists(_MODEL_PATH) and os.path.getsize(_MODEL_PATH) > 0:
        return
    print("Downloading face_landmarker.task model (first run only)...")
    urllib.request.urlretrieve(_MODEL_URL, _MODEL_PATH)
    print("Model downloaded to", _MODEL_PATH)


class FaceMeshDetector:
    def __init__(self, max_faces=1, min_detection_confidence=0.5,
                 min_tracking_confidence=0.5, min_presence_confidence=0.5):
        _ensure_model()

        options = FaceLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=_MODEL_PATH),
            running_mode=RunningMode.VIDEO,
            num_faces=max_faces,
            min_face_detection_confidence=min_detection_confidence,
            min_face_presence_confidence=min_presence_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self.landmarker = FaceLandmarker.create_from_options(options)
        self._start_time = time.monotonic()
        self._last_timestamp_ms = -1

    def _next_timestamp_ms(self):
        
        ts = int((time.monotonic() - self._start_time) * 1000)
        if ts <= self._last_timestamp_ms:
            ts = self._last_timestamp_ms + 1
        self._last_timestamp_ms = ts
        return ts

    def process(self, frame_bgr):
       
        h, w = frame_bgr.shape[:2]
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        result = self.landmarker.detect_for_video(mp_image, self._next_timestamp_ms())

        if not result.face_landmarks:
            return None

        face_landmarks = result.face_landmarks[0]  # first detected face
        points = np.array(
            [(lm.x * w, lm.y * h) for lm in face_landmarks],
            dtype=np.float64,
        )

        return {
            "all": points,
            "left_eye": points[LEFT_EYE],
            "right_eye": points[RIGHT_EYE],
            "left_iris": points[LEFT_IRIS],
            "right_iris": points[RIGHT_IRIS],
            "left_iris_center": points[LEFT_IRIS].mean(axis=0),
            "right_iris_center": points[RIGHT_IRIS].mean(axis=0),
            "left_corners": (points[LEFT_EYE_CORNERS[0]], points[LEFT_EYE_CORNERS[1]]),
            "right_corners": (points[RIGHT_EYE_CORNERS[0]], points[RIGHT_EYE_CORNERS[1]]),
            "left_lids": (points[LEFT_EYE_LIDS[0]], points[LEFT_EYE_LIDS[1]]),
            "right_lids": (points[RIGHT_EYE_LIDS[0]], points[RIGHT_EYE_LIDS[1]]),
        }

    def close(self):
        self.landmarker.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()