
from collections import deque
import time


class AttentionScorer:
    def __init__(self, window_seconds=5.0, min_samples=5):
        self.window_seconds = window_seconds
        self.min_samples = min_samples
        # each entry: (timestamp, is_attentive: bool)
        self._history = deque()

    def update(self, gaze_result):
        """
        Feed the latest GazeResult in. "Attentive" = direction is 'center'.
        Blinking is treated as neutral (kept as the last known state) since
        a blink shouldn't count as looking away.
        """
        now = time.time()

        if gaze_result.direction == "no_face":
            attentive = False
        elif gaze_result.direction == "blinking":
            attentive = self._history[-1][1] if self._history else True
        else:
            attentive = gaze_result.direction == "center"

        self._history.append((now, attentive))
        self._trim(now)

        return self.score()

    def _trim(self, now):
        while self._history and (now - self._history[0][0]) > self.window_seconds:
            self._history.popleft()

    def score(self):
        """Returns attention score in [0, 1], or None if not enough data yet."""
        if len(self._history) < self.min_samples:
            return None
        attentive_count = sum(1 for _, a in self._history if a)
        return attentive_count / len(self._history)

    def label(self):
        score = self.score()
        if score is None:
            return "calibrating..."
        if score >= 0.75:
            return "focused"
        if score >= 0.4:
            return "distracted"
        return "not paying attention"