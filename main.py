"""

Controls:
  q / ESC  -> quit
  l        -> toggle full face-mesh landmark overlay
  c        -> recalibrate neutral gaze position (look at the screen, then press)
  [        -> increase sensitivity (catch smaller/subtler eye movements)
  ]        -> decrease sensitivity (ignore small jitter, require a bigger glance)
"""

import cv2

from camera import Camera
from face_mesh import FaceMeshDetector
from gaze import GazeTracker
from attention import AttentionScorer
from utils import draw_landmarks, draw_iris, put_label

WINDOW_NAME = "IRIS"
AUTO_CALIBRATE_AFTER_FRAMES = 30  # ~1s at 30fps of continuous face detection


def draw_hud(frame, gaze_result, attention_score, attention_label, fps, calibrated, calibrating_msg, deadzone):
    h, w = frame.shape[:2]

    put_label(frame, f"Gaze: {gaze_result.direction}", (20, 40),
               color=(0, 255, 255))
    put_label(frame, f"H: {gaze_result.h_ratio:.2f}  V: {gaze_result.v_ratio:.2f}",
               (20, 70), color=(200, 200, 200), scale=0.5)
    put_label(frame, f"EAR L:{gaze_result.left_ear:.2f} R:{gaze_result.right_ear:.2f}",
               (20, 95), color=(200, 200, 200), scale=0.5)

    score_text = "Attention: --" if attention_score is None else f"Attention: {attention_score*100:.0f}%"
    color = (0, 255, 0)
    if attention_score is not None:
        color = (0, 255, 0) if attention_score >= 0.75 else (0, 165, 255) if attention_score >= 0.4 else (0, 0, 255)
    put_label(frame, score_text, (20, 130), color=color)
    put_label(frame, attention_label, (20, 158), color=color, scale=0.5)

    put_label(frame, f"FPS: {fps:.1f}", (w - 140, 30), color=(150, 150, 150), scale=0.5)
    put_label(frame, f"Sensitivity (deadzone): {deadzone:.3f}  [ / ]",
               (w - 260, 55), color=(150, 150, 150), scale=0.45)

    if calibrating_msg:
        put_label(frame, calibrating_msg, (20, h - 50), color=(0, 255, 255), scale=0.6)
    elif not calibrated:
        put_label(frame, "Look at the screen, then press 'c' to calibrate",
                   (20, h - 50), color=(0, 165, 255), scale=0.55)
    else:
        put_label(frame, "Press 'c' to recalibrate", (20, h - 20),
                   color=(120, 120, 120), scale=0.45)


def main():
    show_full_mesh = False
    face_seen_frames = 0
    calibrating_msg_timer = 0  # frames left to show a "Calibrated!" flash

    with Camera(source=0) as camera, FaceMeshDetector() as detector:
        gaze_tracker = GazeTracker(
            
            smoothing_alpha=0.8
        )
        attention_scorer = AttentionScorer(window_seconds=5.0)

        prev_time = cv2.getTickCount()
        tick_freq = cv2.getTickFrequency()

        while True:
            success, frame = camera.read()
            if not success:
                print("Failed to read from camera.")
                break

            landmarks = detector.process(frame)
            gaze_result = gaze_tracker.update(landmarks)

            # --- Auto-calibrate shortly after the face is first steadily seen ---
            if landmarks is not None:
                face_seen_frames += 1
                if not gaze_tracker.is_calibrated and face_seen_frames == AUTO_CALIBRATE_AFTER_FRAMES:
                    gaze_tracker.calibrate_center()
                    calibrating_msg_timer = 30
            else:
                face_seen_frames = 0

            attention_score = attention_scorer.update(gaze_result)
            attention_label = attention_scorer.label()

            if landmarks is not None:
                pass

            now = cv2.getTickCount()
            fps = tick_freq / (now - prev_time) if now != prev_time else 0.0
            prev_time = now

            calibrating_msg = "Calibrated!" if calibrating_msg_timer > 0 else None
            if calibrating_msg_timer > 0:
                calibrating_msg_timer -= 1

            draw_hud(frame, gaze_result, attention_score, attention_label, fps,
                      gaze_tracker.is_calibrated, calibrating_msg, gaze_tracker.h_deadzone)

            cv2.imshow(WINDOW_NAME, frame)
            key = cv2.waitKey(1) & 0xFF
            small_frame = cv2.resize(frame, (640, 480)) 
            if key in (ord('q'), 27):  # 'q' or ESC
                break
            elif key == ord('l'):
                show_full_mesh = not show_full_mesh
            elif key == ord('c'):
                gaze_tracker.calibrate_center()
                calibrating_msg_timer = 30
            elif key == ord('['):
                gaze_tracker.increase_sensitivity()
            elif key == ord(']'):
                gaze_tracker.decrease_sensitivity()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()