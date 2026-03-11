import sys
import os
import cv2
from PyQt5.QtWidgets import QApplication

from hand_detector import HandDetector
from controlled_ball_system import ControlledBallSystem
from ui.main_window import GameUI


def initialize_camera():
    """Pick a working camera, preferring external devices over built-in."""
    env_index = os.getenv("CAMERA_INDEX")
    if env_index is not None:
        try:
            forced_index = int(env_index)
            cap = cv2.VideoCapture(forced_index, cv2.CAP_DSHOW)
            if cap.isOpened():
                print(f"Using forced camera index: {forced_index}")
                return cap
            cap.release()
        except ValueError:
            print("Invalid CAMERA_INDEX value. Falling back to auto-detection.")

    # Prefer external camera first (usually index 1/2), then fallback to built-in.
    for cam_index in [1, 2, 0, 3, 4]:
        cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
        if cap.isOpened():
            print(f"Using camera index: {cam_index}")
            return cap
        cap.release()

    raise RuntimeError(
        "No camera found. Connect a webcam and optionally set CAMERA_INDEX."
    )


def main():
    cap = initialize_camera()

    detector = HandDetector()

    game = ControlledBallSystem(cap, detector)

    app = QApplication(sys.argv)

    window = GameUI(game)
    window.showMaximized()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()