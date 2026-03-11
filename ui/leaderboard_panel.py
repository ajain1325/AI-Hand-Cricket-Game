from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy
from PyQt5.QtCore import Qt


class LeaderboardPanel(QWidget):

    def __init__(self):
        super().__init__()
        # BACKGROUND WALLPAPER
        self.setStyleSheet("""
        QWidget{
            border-image: url(border1.jpg) 0 0 0 0 stretch stretch;
        }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(10,10,10,10)
        # -------- LEADERBOARD --------
        lb_title = QLabel("LEADERBOARD")
        lb_title.setStyleSheet("font-size:20px;font-weight:bold;color:white;")

        self.leaderboard = QTableWidget()
        self.leaderboard.setColumnCount(3)
        self.leaderboard.setHorizontalHeaderLabels(["Rank","Player Name","Score"])
        self.leaderboard.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.leaderboard.verticalHeader().setVisible(False)
        self.leaderboard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.leaderboard.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.leaderboard.setEditTriggers(QTableWidget.NoEditTriggers)
        self.leaderboard.setSelectionMode(QTableWidget.NoSelection)
        self.leaderboard.setMaximumHeight(150)

        self.leaderboard.setStyleSheet("""
        QTableWidget{
            background: rgba(255,255,255,0.92);
            border-radius:8px;
        }

        QHeaderView::section{
            background:#1f3c88;
            color:white;
            font-weight:bold;
        }
        """)

        # -------- SCOREBOARD --------
        score_title = QLabel("SCOREBOARD")
        score_title.setStyleSheet("font-size:20px;font-weight:bold;color:white;")

        self.score_box = QFrame()
        self.score_box.setStyleSheet("""
        background:rgba(255,255,255,0.92);
        border-radius:10px;
        padding:5px;                             
        """)

        self.score_player = QLabel("Player : -")
        self.score_player.setStyleSheet("font-size:16px;font-weight:bold;padding:8px 8px 2px 8px;")

        self.score = QTableWidget()
        self.score.setRowCount(2)
        self.score.setColumnCount(8)
        self.score.setHorizontalHeaderLabels(["Type", "1", "2", "3", "4", "5", "6", "Total"])
        self.score.verticalHeader().setVisible(False)
        self.score.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.score.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.score.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.score.setEditTriggers(QTableWidget.NoEditTriggers)
        self.score.setSelectionMode(QTableWidget.NoSelection)
        self.score.setMaximumHeight(110)

        self.score.setItem(0, 0, QTableWidgetItem("Player"))
        self.score.setItem(1, 0, QTableWidgetItem("AI"))
        for col in range(1, 7):
            self.score.setItem(0, col, QTableWidgetItem("-"))
            self.score.setItem(1, col, QTableWidgetItem("-"))
        self.score.setItem(0, 7, QTableWidgetItem("0"))
        self.score.setItem(1, 7, QTableWidgetItem("-"))

        for row in range(2):
            for col in range(8):
                item = self.score.item(row, col)
                if item:
                    item.setTextAlignment(Qt.AlignCenter)

        score_layout = QVBoxLayout()
        score_layout.addWidget(self.score_player)
        score_layout.addWidget(self.score)
        self.score_box.setLayout(score_layout)

        # -------- AI ADAPTATION --------
        ai_title = QLabel("AI ADAPTATION")
        ai_title.setStyleSheet("font-size:20px;font-weight:bold;color:white;")

        self.ai_box = QFrame()
        self.ai_box.setStyleSheet("""
        background:rgba(255,255,255,0.92);
        border-radius:10px;
        padding:6px;
        """)
        self.ai_box.setMaximumHeight(120)

        self.ai_info = QLabel("The AI Strategy Selection engine transitions from a Random Phase at initialization "
                                      "to an Adaptive Phase as gameplay continues. By storing every player move in a history "
                                                      "array, the system utilizes weighted probability to predict human patterns.")
        self.ai_info.setStyleSheet("""
                                   padding:10px;
                                    font-size:15px;
                                   font-weight:bold;
                                    color:#333333;
                                    line-height:18px;
                                    """)
        self.ai_info.setWordWrap(True)

        ai_layout = QVBoxLayout()
        ai_layout.addWidget(self.ai_info)
        self.ai_box.setLayout(ai_layout)

        # -------- ADD TO LAYOUT --------
        layout.addWidget(lb_title)
        layout.addWidget(self.leaderboard,3)

        layout.addWidget(score_title)
        layout.addWidget(self.score_box,2)

        layout.addWidget(ai_title)
        layout.addWidget(self.ai_box,1)

        self.setLayout(layout)