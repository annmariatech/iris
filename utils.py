

import cv2
import numpy as np


def euclidean(p1, p2):
    return float(np.linalg.norm(np.array(p1) - np.array(p2)))


def eye_aspect_ratio(top, bottom, outer, inner):
    """
    Simplified EAR using one vertical pair and the horizontal corners.
    Lower values = eye more closed. Typical open-eye EAR ~0.25-0.35,
    closed-eye EAR drops below ~0.15-0.18 (tune per-user).
    """
    vertical = euclidean(top, bottom)
    horizontal = euclidean(outer, inner)
    if horizontal == 0:
        return 0.0
    return vertical / horizontal


def iris_position_ratio(iris_center, outer_corner, inner_corner):
    """
    Returns the normalized horizontal position of the iris between the
    two eye corners.

    0.0 -> outer corner
    0.5 -> center
    1.0 -> inner corner
    """

    eye_width = inner_corner[0] - outer_corner[0]

    if abs(eye_width) < 1e-6:
        return 0.5

    ratio = (iris_center[0] - outer_corner[0]) / eye_width

    return float(np.clip(ratio, 0.0, 1.0))



class EMASmoother:
    """Exponential moving average smoother for noisy per-frame values/points."""

    def __init__(self, alpha=0.4):
        self.alpha = alpha
        self.value = None

    def update(self, new_value):
        new_value = np.array(new_value, dtype=np.float64)
        if self.value is None:
            self.value = new_value
        else:
            self.value = self.alpha * new_value + (1 - self.alpha) * self.value
        return self.value


def draw_landmarks(frame, points, color=(0, 255, 0), radius=1):
    for (x, y) in points:
        cv2.circle(frame, (int(x), int(y)), radius, color, -1, cv2.LINE_AA)


def draw_iris(frame, iris_points, color=(0, 255, 255)):
    center = iris_points.mean(axis=0)
    radius = np.mean([euclidean(p, center) for p in iris_points])
    cv2.circle(frame, (int(center[0]), int(center[1])), int(radius), color, 1, cv2.LINE_AA)
    cv2.circle(frame, (int(center[0]), int(center[1])), 2, color, -1, cv2.LINE_AA)


def put_label(frame, text, org, color=(255, 255, 255), scale=0.6, thickness=2):
    cv2.putText(frame, text, org, cv2.FONT_HERSHEY_SIMPLEX, scale,
                (0, 0, 0), thickness + 2, cv2.LINE_AA)  # outline
    cv2.putText(frame, text, org, cv2.FONT_HERSHEY_SIMPLEX, scale,
                color, thickness, cv2.LINE_AA)