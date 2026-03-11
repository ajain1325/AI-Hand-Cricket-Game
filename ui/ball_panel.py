from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QFrame, QToolButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt


class BallPanel(QWidget):

    def __init__(self):
        super().__init__()

        self.buttons = {}

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        title = QLabel("BALL")
        title.setAlignment(Qt.AlignCenter)
        title.setContentsMargins(0, 0, 0, 0)
        title.setStyleSheet("font-size:24px;font-weight:bold;padding:0px;margin:0px;")

        board = QFrame()
        board.setStyleSheet("""
        QFrame{
            border-image: url(images10.jpg) 0 0 0 0 stretch stretch;
            border-radius:10px;
        }
        """)

        layout = QGridLayout()
        layout.setHorizontalSpacing(8)
        layout.setVerticalSpacing(8)
        layout.setContentsMargins(8, 8, 8, 8)

        nums=[1,2,3,4,5,6]
        pos=[(0,0),(0,1),(1,0),(1,1),(2,0),(2,1)]

        for n,p in zip(nums,pos):

            btn = QToolButton()
            btn.setToolTip(f"Ball {n}")
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            btn.setText(f"Ball {n}")

            btn.setStyleSheet("""
                QToolButton{
                    height:150px;
                    width:150px;
                    padding:0px;
                    border:2px solid #c8c8c8;
                    font-size:14px;
                    font-weight:bold;
                    color:#111;
                }
            """)

            layout.addWidget(btn,p[0],p[1])

            self.buttons[n] = btn

        board.setLayout(layout)

        main_layout.addWidget(title)
        main_layout.addWidget(board, 1)
        self.setLayout(main_layout)
    
    def reset_balls(self):
        for n, btn in self.buttons.items():
            btn.setIcon(QIcon())     # remove image
            btn.setText(f"Ball {n}") # restore default label

    # ⭐ NEW FUNCTION: show captured frame
    def set_ball_image(self, ball_number, frame, detected_number=None):

        if ball_number not in self.buttons:
            return

        btn = self.buttons[ball_number]

        height, width, channel = frame.shape
        bytesPerLine = channel * width

        from PyQt5.QtGui import QImage
        qImg = QImage(frame.data,width,height,bytesPerLine,QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(qImg)

        pixmap = pixmap.scaled(
            btn.width()-6, btn.height()-6,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )

        btn.setIcon(QIcon(pixmap))
        btn.setIconSize(btn.size())
        if detected_number is not None:
            btn.setText(f"Ball {ball_number}\n{detected_number}")