import cv2
import time
import random
from collections import Counter

# from seaborn import heatmap
from gesture_visualizer import GestureVisualizer
class ControlledBallSystem:

    def __init__(self, cap, detector):
        self.cap = cap
        self.detector = detector
        self.score = 0
        self.balls = 6
        self.player_history = []
        self.ball_results = []
        self.player_name = ""
        self.visualizer = GestureVisualizer()
        self.heatmaps = []

    # ---------------- Add Welcome Screen Function ---------------- #
    def welcome_screen(self):

        start = time.time()

        while time.time() - start < 5:

            ret, frame = self.cap.read()
            if not ret:
                continue
            frame = cv2.flip(frame, 1)

            cv2.putText(frame,"WELCOME TO AI HAND CRICKET",
                        (120,200),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,(0,255,255),3)

            cv2.putText(frame,f"Hello {self.player_name}!",
                        (200,260),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,(0,255,0),2)

            cv2.putText(frame,"Match starts in 5 seconds...",
                        (150,320),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,(255,255,255),2)

            cv2.imshow("AI Hand Cricket",frame)
            cv2.waitKey(1)

    # ---------------- PLAYER NAME ---------------- #
    def get_player_name(self):
        self.player_name = input("Enter Player Name: ")
        if self.player_name.strip() == "":
            self.player_name = "Player"

    # ---------------- COUNTDOWN ---------------- #
    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            start = time.time()
            while time.time() - start < 1:
                ret, frame = self.cap.read()
                if not ret:
                    continue
                frame = cv2.flip(frame, 1)

                cv2.putText(frame, str(i),
                            (300, 300),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            5, (0, 0, 255), 10)

                cv2.imshow("AI Hand Cricket", frame)
                cv2.waitKey(1)

    # ---------------- AI LOGIC ---------------- #
    def ai_move(self):
        if len(self.player_history) < 2:
            return random.randint(0, 6), "Random"
        else:
            freq = Counter(self.player_history)
            most_common = freq.most_common(1)[0][0]

            if random.random() < 0.6:
                return most_common, "Predicted Frequent"
            else:
                return random.randint(0, 6), "Random Variation"

    # ---------------- SAVE SCORE ---------------- #
    def save_score(self):
        with open("leaderboard.txt", "a") as f:
            f.write(f"{self.player_name},{self.score}\n")

    # ---------------- LOAD TOP 10 ---------------- #
    def get_top_players(self):
        return self.get_sorted_players(limit=10)

    # ---------------- LOAD SORTED PLAYERS ---------------- #
    def get_sorted_players(self, limit=None):
        players = []
        try:
            with open("leaderboard.txt", "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or "," not in line:
                        continue
                    name, score = line.split(",", 1)
                    players.append((name, int(score)))
        except:
            pass

        players.sort(key=lambda x: x[1], reverse=True)
        if limit is None:
            return players
        return players[:limit]

    # ---------------- MAIN GAME ---------------- #
    def play_game(self):

        self.score = 0
        self.player_history = []
        self.ball_results = []

        self.get_player_name()
        self.welcome_screen()
        for ball in range(self.balls):

            self.countdown(3)
            time.sleep(0.2)

            ret, frame = self.cap.read()
            if not ret:
                continue
            frame = cv2.flip(frame, 1)

            results = self.detector.find_hand(frame)
            if not results or not results.multi_hand_landmarks:
                continue
            player_number, finger_states = self.detector.count_fingers(frame, results)
            heatmap = self.visualizer.create_heatmap(frame, finger_states, player_number)
            self.heatmaps.append((ball+1, heatmap))
            cv2.imshow("AI Vision - Finger Heatmap", heatmap)
            cv2.waitKey(1)

            




            self.player_history.append(player_number)
            ai_number, ai_reason = self.ai_move()

            if player_number == ai_number and player_number != 0:
                result_text = "OUT!"
                self.ball_results.append((ball+1, player_number, ai_number, "OUT"))
            else:
                self.score += player_number
                result_text = f"Total: {self.score}"
                self.ball_results.append((ball+1, player_number, ai_number, self.score))

            # -------- RESULT DISPLAY -------- #
            start = time.time()
            while time.time() - start < 2:

                ret, frame = self.cap.read()
                if not ret:
                    continue
                frame = cv2.flip(frame, 1)

                # Header
                cv2.putText(frame, f"{self.player_name} Score: {self.score}",
                            (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2)

                # Current Ball Info
                cv2.putText(frame, f"Ball {ball+1}/6",
                            (10, 80),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (255, 255, 0), 2)

                cv2.putText(frame, f"Player: {player_number}",
                            (10, 120),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (255, 0, 0), 2)

                cv2.putText(frame, f"AI: {ai_number}",
                            (10, 160),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (0, 0, 255), 2)
                cv2.putText(frame, f"AI Mode: {ai_reason}",
                            (10, 190),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, (200,200,200), 1)
                # Ball History Panel
                y_offset = 220
                cv2.putText(frame, "Ball History:",
                            (10, y_offset),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (0, 255, 255), 2)

                y_offset += 30
                for result in self.ball_results:
                    ball_no, p_run, ai_run, total = result
                    
                    
                    if total == "OUT":
                        text = f"B{ball_no}: P={p_run} AI={ai_run}  OUT"
                    else:
                        text = f"B{ball_no}: P={p_run} AI={ai_run}  Total={total}"

                    cv2.putText(frame, text,
                                (10, y_offset),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.6, (255, 255, 255), 1)
                    y_offset += 25

                cv2.imshow("AI Hand Cricket", frame)
                cv2.waitKey(1)

            if player_number == ai_number and player_number != 0:
                break

        # Save score
        self.save_score()
        self.show_match_summary()
        # -------- SHOW HEATMAP ANALYSIS --------
        for ball_no, heatmap in self.heatmaps:
            cv2.imshow(f"Ball {ball_no} Heatmap", heatmap)

        top_players = self.get_top_players()

        # -------- LEADERBOARD SCREEN -------- #
        while True:
            ret, frame = self.cap.read()
            if not ret:
                continue
            frame = cv2.flip(frame, 1)

            cv2.putText(frame, "TOP 10 PLAYERS",
                        (150, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.2, (0, 255, 255), 3)

            y = 100
            rank = 1
            for name, score in top_players:
                text = f"{rank}. {name} - {score}"
                cv2.putText(frame, text,
                            (100, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (0, 255, 0), 2)
                y += 40
                rank += 1

            cv2.putText(frame, "Press ESC to Exit",
                        (150, 420),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 0, 255), 2)

            cv2.imshow("AI Hand Cricket", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break
        
        
    # -------- Match Summary Screen -------- #
    def show_match_summary(self):

        while True:

            ret, frame = self.cap.read()
            if not ret:
                continue
            frame = cv2.flip(frame, 1)

            cv2.putText(frame,"MATCH SUMMARY",
                        (180,60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.2,(0,255,255),3)

            cv2.putText(frame,f"Player: {self.player_name}",
                        (50,120),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,(0,255,0),2)

            cv2.putText(frame,f"Total Score: {self.score}",
                        (50,160),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,(0,255,0),2)

            y = 220

            for result in self.ball_results:

                ball_no, p_run, ai_run, total = result

                text = f"Ball {ball_no}: Player={p_run} AI={ai_run}"

                cv2.putText(frame,text,
                            (50,y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,(255,255,255),2)

                y += 35

            cv2.putText(frame,"Press ENTER to view Leaderboard",
                        (120,420),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,(0,0,255),2)

            cv2.imshow("AI Hand Cricket",frame)

            key = cv2.waitKey(1)

            if key == 13 or key == 10:   # ENTER
                break
