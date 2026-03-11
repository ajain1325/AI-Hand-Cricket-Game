from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QInputDialog
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt

from ui.ball_panel import BallPanel
from ui.center_panel import CenterPanel
from ui.leaderboard_panel import LeaderboardPanel


class GameUI(QMainWindow):

    def __init__(self, game):
        super().__init__()

        self.game = game

        self.setWindowTitle("AI Hand Cricket")

        # -------- PLAYER NAME --------
        name, ok = QInputDialog.getText(self, "Player Name", "Enter your name:")

        if ok and name.strip() != "":
            self.game.player_name = name
        else:
            self.game.player_name = "Player"

        main_widget = QWidget()
        layout = QHBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(12,12,12,12)

        self.ball_panel = BallPanel()
        self.center_panel = CenterPanel(self.game)
        self.leaderboard_panel = LeaderboardPanel()
        self.leaderboard_panel.leaderboard.setFixedHeight(220)
        self.leaderboard_panel.leaderboard.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.leaderboard_panel.ai_box.setMaximumHeight(140)

        layout.addWidget(self.ball_panel, 2)
        layout.addWidget(self.center_panel, 5)
        layout.addWidget(self.leaderboard_panel, 3)

        main_widget.setLayout(layout)

        self.setStyleSheet("""
        QMainWindow{
            background:#f4f6f8;
        }

        QFrame{
            background:#ffffff;
            border:1px solid #d9d9d9;
            border-radius:8px;
        }

        QTableWidget{
            background:white;
            gridline-color:#eeeeee;
        }

        QHeaderView::section{
            background:#1f3c88;
            color:white;
            font-weight:bold;
        }
        """)
        self.setStyleSheet("""
        QMainWindow{
            border-image: url(.jpg) 0 0 0 0 stretch stretch;
        }
        """)

        self.setCentralWidget(main_widget)

        # -------- INITIAL SCORECARD --------
        self.update_scoreboard(
            self.game.player_name,
            ["-"] * 6,
            ["-"] * 6,
            0
        )

        # -------- LOAD LEADERBOARD --------
        self.refresh_leaderboard()

    # Show captured hand posture image in the detected ball slot.
    def show_ball_image(self, num, frame, detected_number=None):
        self.ball_panel.set_ball_image(num, frame, detected_number)

    def refresh_leaderboard(self):

        self.leaderboard_panel.leaderboard.setRowCount(0)

        players = self.game.get_sorted_players(limit=5)

        self.leaderboard_panel.leaderboard.setRowCount(len(players))

        for row,(name,score) in enumerate(players):

            rank_item = QTableWidgetItem(str(row+1))
            name_item = QTableWidgetItem(str(name))
            score_item = QTableWidgetItem(str(score))

            rank_item.setTextAlignment(Qt.AlignCenter)
            name_item.setTextAlignment(Qt.AlignCenter)
            score_item.setTextAlignment(Qt.AlignCenter)

            self.leaderboard_panel.leaderboard.setItem(row,0,rank_item)
            self.leaderboard_panel.leaderboard.setItem(row,1,name_item)
            self.leaderboard_panel.leaderboard.setItem(row,2,score_item)

    # -------- UPDATE SCOREBOARD --------
    def update_scoreboard(self, name, player_runs, ai_runs, total):
        self.leaderboard_panel.score_player.setText(f"Player : {name}")

        # Fill ball-by-ball values into scoreboard table columns 1..6.
        for idx in range(6):
            p_item = QTableWidgetItem(str(player_runs[idx]))
            a_item = QTableWidgetItem(str(ai_runs[idx]))
            p_item.setTextAlignment(Qt.AlignCenter)
            a_item.setTextAlignment(Qt.AlignCenter)
            self.leaderboard_panel.score.setItem(0, idx + 1, p_item)
            self.leaderboard_panel.score.setItem(1, idx + 1, a_item)

        p_total = QTableWidgetItem(str(total))
        p_total.setTextAlignment(Qt.AlignCenter)
        self.leaderboard_panel.score.setItem(0, 7, p_total)