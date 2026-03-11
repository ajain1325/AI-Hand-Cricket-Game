import cv2

class GestureVisualizer:

    def create_heatmap(self, frame, fingers, gesture_number):

        vis_frame = frame.copy()

        finger_names = ["Thumb","Index","Middle","Ring","Pinky"]

        y = 60

        for i, state in enumerate(fingers):

            if state == 1:
                color = (0,255,0)
                status = "OPEN"
            else:
                color = (0,0,255)
                status = "CLOSED"

            text = f"{finger_names[i]} : {status}"

            cv2.putText(vis_frame,
                        text,
                        (20,y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        color,
                        2)

            y += 40

        cv2.putText(vis_frame,
                    f"Detected Gesture: {gesture_number}",
                    (20,280),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255,255,0),
                    2)

        return vis_frame