"""
gaze.py
Turns raw face-mesh + iris landmarks into a gaze direction estimate
and blink detection, with light temporal smoothing.

Where the iris naturally sits when looking straight at the camera
varies a lot per person/webcam (angle, height, face shape), so instead
of fixed absolute thresholds this calibrates against the user's own
neutral position: call calibrate_center() once while they're looking
at the screen, and direction is classified relative to that baseline.
"""

from dataclasses import dataclass

from utils import eye_aspect_ratio, iris_position_ratio, EMASmoother

BLINK_EAR_THRESHOLD = 0.19

# How far (in ratio units, ~0-1 scale) the iris must move from the
# calibrated center before it counts as looking away. Smaller = more
# sensitive (catches subtle corner-of-the-eye glances). Larger = less
# sensitive (ignores small jitter, only flags clear head/eye turns).
DEFAULT_H_DEADZONE = 0.025
DEFAULT_V_DEADZONE = 0.03

MIN_DEADZONE = 0.01
MAX_DEADZONE = 0.15
DEADZONE_STEP = 0.01


@dataclass
class GazeResult:
    direction: str          # "left" | "right" | "up" | "down" | "center" | "blinking" | "no_face"
    h_ratio: float           # raw horizontal iris ratio for this frame
    v_ratio: float           # raw vertical iris ratio for this frame
    left_ear: float
    right_ear: float
    is_blinking: bool


class GazeTracker:
    def __init__(self, smoothing_alpha=0.5, h_deadzone=DEFAULT_H_DEADZONE,
                 v_deadzone=DEFAULT_V_DEADZONE):
        self.h_smoother = EMASmoother(alpha=smoothing_alpha)
        self.v_smoother = EMASmoother(alpha=smoothing_alpha)
        self.h_deadzone = h_deadzone
        self.v_deadzone = v_deadzone

        # Neutral/"looking at camera" baseline - set via calibrate_center().
        # Defaults to 0.5 so the tracker is still usable before calibrating.
        self.h_center = 0.5
        self.v_center = 0.5
        self.is_calibrated = False

        self._last_h_ratio = 0.5
        self._last_v_ratio = 0.5

    def update(self, landmarks):
        """
        landmarks: dict returned by FaceMeshDetector.process(), or None.
        Returns a GazeResult.
        """
        if landmarks is None:
            return GazeResult("no_face", self._last_h_ratio, self._last_v_ratio, 0.0, 0.0, False)

        # --- Blink detection (average of both eyes' EAR) ---
        l_top, l_bottom = landmarks["left_lids"]
        l_outer, l_inner = landmarks["left_corners"]
        r_top, r_bottom = landmarks["right_lids"]
        r_inner, r_outer = landmarks["right_corners"]  # note order for right eye

        left_ear = eye_aspect_ratio(l_top, l_bottom, l_outer, l_inner)
        right_ear = eye_aspect_ratio(r_top, r_bottom, r_outer, r_inner)
        avg_ear = (left_ear + right_ear) / 2.0
        is_blinking = avg_ear < BLINK_EAR_THRESHOLD

        if is_blinking:
            return GazeResult("blinking", self._last_h_ratio, self._last_v_ratio,
                               left_ear, right_ear, True)

        # --- Horizontal gaze ratio, averaged across both eyes ---
        left_h = iris_position_ratio(landmarks["left_iris_center"], l_outer, l_inner)
        right_h = iris_position_ratio(landmarks["right_iris_center"], r_outer, r_inner)
        h_ratio = (left_h + right_h) / 2.0

        # --- Vertical gaze ratio, averaged across both eyes ---
        left_v = iris_position_ratio(landmarks["left_iris_center"], l_top, l_bottom)
        right_v = iris_position_ratio(landmarks["right_iris_center"], r_top, r_bottom)
        v_ratio = (left_v + right_v) / 2.0

        h_ratio = float(self.h_smoother.update(h_ratio))
        v_ratio = float(self.v_smoother.update(v_ratio))

        self._last_h_ratio = h_ratio
        self._last_v_ratio = v_ratio

        direction = self._classify(h_ratio, v_ratio)

        return GazeResult(direction, h_ratio, v_ratio, left_ear, right_ear, False)

    def calibrate_center(self):
        """
        Call this while the person is looking straight at the camera/screen
        to (re)set the neutral gaze baseline. Safe to call repeatedly
        (e.g. bound to a keypress) if the camera or seating position changes.
        """
        self.h_center = self._last_h_ratio
        self.v_center = self._last_v_ratio
        self.is_calibrated = True

    def increase_sensitivity(self):
        """Shrinks the deadzone so smaller eye movements register as 'looking away'."""
        self.h_deadzone = max(MIN_DEADZONE, self.h_deadzone - DEADZONE_STEP)
        self.v_deadzone = max(MIN_DEADZONE, self.v_deadzone - DEADZONE_STEP)

    def decrease_sensitivity(self):
        """Widens the deadzone so only larger eye movements register as 'looking away'."""
        self.h_deadzone = min(MAX_DEADZONE, self.h_deadzone + DEADZONE_STEP)
        self.v_deadzone = min(MAX_DEADZONE, self.v_deadzone + DEADZONE_STEP)

    def _classify(self, h_ratio, v_ratio):
        dh = h_ratio - self.h_center
        dv = v_ratio - self.v_center

        if dh < -self.h_deadzone:
            return "left"
        if dh > self.h_deadzone:
            return "right"
        if dv < -self.v_deadzone:
            return "up"
        if dv > self.v_deadzone:
            return "down"
        return "center"