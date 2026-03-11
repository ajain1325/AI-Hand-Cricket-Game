import cv2
import time
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton, QInputDialog
class CenterPanel(QWidget):

    def __init__(self, game):
        super().__init__()
        
        

        self.game = game
        self.cap = game.cap

        # -------- GAME STATE --------
        self.ball = 0
        self.max_balls = 6
        self.player_score = 0

        self.countdown_start = time.time()
        self.detected = False

        self.player_runs = ["-"] * 6
        self.ai_runs = ["-"] * 6
        self.game_saved = False

        self.last_detection = 0

        layout = QVBoxLayout()

        # ---------------- RULES ----------------
        rules_title = QLabel("HAND CRICKET")
        rules_title.setStyleSheet("""
        font-size:24px;
        font-weight:bold;
        color:white;
        """)

        rules = QTextEdit()
        rules.setStyleSheet("""
        QTextEdit{
            border-image: url(gemini.png) 0 0 0 0 stretch stretch;
            border-radius:10px;
            padding:8px;
            font-size:14px;
            color:white;
        }
        """)
        rules.setReadOnly(True)
        
        # ---------------- CAMERA ----------------
        self.camera_label = QLabel()
        self.camera_label.setMinimumHeight(350)
        self.camera_label.setStyleSheet("""
        background:black;
        border-radius:10px;
        border:2px solid white;
        """)
        self.camera_label.setAlignment(Qt.AlignCenter)

        # ---------------- DECISION WINDOW ----------------
        decision_title = QLabel("DECISION WINDOW")
        decision_title.setStyleSheet("font-size:20px;font-weight:bold")

        self.decision = QLabel("Waiting...")
        self.restart_btn = QPushButton("Restart Game")
        self.restart_btn.setStyleSheet("""
        font-size:18px;
        padding:8px;
        background:#1f3c88;
        color:white;
        border-radius:8px;
        """)
        self.restart_btn.hide()
        self.restart_btn.clicked.connect(self.restart_game)

        self.decision.setStyleSheet("""
        font-size:26px;
        color:red;
        font-weight:bold;
        background:rgba(255,255,255,0.85);
        border-radius:8px;
        padding:6px;
        """)

        layout.addWidget(rules_title)
        layout.addWidget(rules, 2)
        layout.addWidget(self.camera_label, 3)
        layout.addWidget(decision_title)
        layout.addWidget(self.decision)
        layout.addWidget(self.restart_btn)

        self.setLayout(layout)

        # -------- CAMERA TIMER --------
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def _get_game_ui(self):
        # `self.window()` returns the top-level QMainWindow (GameUI).
        return self.window()



    def update_frame(self):

        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame,1)

        # Run hand detection for live preview and game logic.
        results = self.game.detector.find_hand(frame)
        if results and results.multi_hand_landmarks:
            for hand_lms in results.multi_hand_landmarks:
                self.game.detector.mpDraw.draw_landmarks(
                    frame,
                    hand_lms,
                    self.game.detector.mpHands.HAND_CONNECTIONS
                )

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h,w,ch = rgb.shape
        bytes_per_line = ch*w
        qt_image = QImage(rgb.data,w,h,bytes_per_line,QImage.Format_RGB888)
        camera_pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = camera_pixmap.scaled(
            self.camera_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.camera_label.setPixmap(scaled_pixmap)

        # stop game
        if self.ball >= self.max_balls:
            self.finish_game_once()
            self.decision.setText("Game Over")
            self.restart_btn.show()
            return

        current_time = time.time()
        elapsed = current_time - self.countdown_start

        # ---------------- COUNTDOWN ----------------
        if elapsed < 3:

            remaining = 3 - int(elapsed)

            self.decision.setText(
                f"Ball {self.ball+1} starting in {remaining}"
            )

            return

        # ---------------- DETECTION ----------------
        if not self.detected:
            if not results or not results.multi_hand_landmarks:
                self.decision.setText(
                    f"Ball {self.ball+1}: No hand detected, show gesture 0-6"
                )
                self.countdown_start = current_time
                return

            player_number, fingers = self.game.detector.count_fingers(frame, results)

            if player_number < 0 or player_number > 6:
                self.decision.setText(
                    f"Ball {self.ball+1}: Invalid gesture, show 0-6"
                )
                self.countdown_start = current_time
                return

            ai_number, reason = self.game.ai_move()

            current_ball = self.ball + 1
            self.ball += 1

            self.player_runs[current_ball-1] = player_number
            self.ai_runs[current_ball-1] = ai_number

            if player_number == ai_number and player_number != 0:

                self.decision.setText(
                    f"Ball {current_ball}: OUT! (Player {player_number} = AI {ai_number})"
                )

                self.ball = self.max_balls

            elif player_number == 0 and ai_number == 0:

                self.decision.setText(
                    f"Ball {current_ball}: Dot ball (0 = 0), not OUT"
                )

            else:

                self.player_score += player_number

                self.decision.setText(
                    f"Ball {current_ball}: Player {player_number} | AI {ai_number}"
                )

            game_ui = self._get_game_ui()
            if hasattr(game_ui, "show_ball_image"):
                # Put each snapshot in the current ball box (1..6).
                game_ui.show_ball_image(current_ball, rgb, player_number)

            self.update_scorecard()
            self.parent().repaint()
            QApplication.processEvents()
            self.detected = True
            self.result_time = current_time

            return

        # ---------------- RESULT DISPLAY ----------------
        if current_time - self.result_time > 2:

            self.detected = False
            self.countdown_start = time.time()

    # -------- SCORECARD UPDATE FUNCTION --------
    def update_scorecard(self):

        self.game.score = self.player_score

        game_ui = self._get_game_ui()
        if hasattr(game_ui, "update_scoreboard"):

            game_ui.update_scoreboard(
                self.game.player_name,
                self.player_runs,
                self.ai_runs,
                self.player_score
            )

    def finish_game_once(self):

        if self.game_saved:
            return

        self.game.score = self.player_score
        self.game.save_score()

        game_ui = self._get_game_ui()
        if hasattr(game_ui, "refresh_leaderboard"):
            game_ui.refresh_leaderboard()

        self.game_saved = True

    def restart_game(self):

        # ask new player name
        name, ok = QInputDialog.getText(self, "Player Name", "Enter player name:")

        if not ok or name.strip() == "":
            name = "Player"

        self.game.player_name = name

        # -------- RESET GAME STATE --------
        self.ball = 0
        self.player_score = 0
        self.player_runs = ["-"] * 6
        self.ai_runs = ["-"] * 6
        self.detected = False
        self.game_saved = False

        # reset countdown
        self.countdown_start = time.time()

        # hide restart button
        self.restart_btn.hide()

        # reset decision window
        self.decision.setText("Ball 1 starting in 3")

        # -------- RESET UI --------
        game_ui = self._get_game_ui()

        # reset scoreboard
        if hasattr(game_ui, "update_scoreboard"):
            game_ui.update_scoreboard(name, ["-"]*6, ["-"]*6, 0)

        # reset ball images
        if hasattr(game_ui, "ball_panel"):
            game_ui.ball_panel.reset_balls()

        # refresh leaderboard (optional)
        if hasattr(game_ui, "refresh_leaderboard"):
            game_ui.refresh_leaderboard()