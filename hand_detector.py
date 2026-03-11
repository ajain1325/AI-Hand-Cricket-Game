import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mpDraw = mp.solutions.drawing_utils

    def find_hand(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        return results

    def count_fingers(self, frame, results):
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                lmList = []
                h, w, c = frame.shape

                for id, lm in enumerate(handLms.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append((id, cx, cy))

                self.mpDraw.draw_landmarks(
                    frame, handLms, self.mpHands.HAND_CONNECTIONS
                )

                fingers = []

                # Thumb (check x-axis)
                if lmList[4][1] > lmList[3][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # Other fingers (check y-axis)
                tips = [8, 12, 16, 20]
                for tip in tips:
                    if lmList[tip][2] < lmList[tip - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                total = sum(fingers)

                # 🔥 Special Cases
                if fingers == [1, 0, 0, 0, 0]:
                    return 6, fingers   # Thumb only = 6

                if total == 0:
                    return 0, fingers   # Closed fist = 0

                return total, fingers

        return 0, [0,0,0,0,0]

        # return finger_count