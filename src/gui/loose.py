from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src import *

class LooseGUI(QWidget):
    def __init__(self, updateWindow) -> None:
        super().__init__()
        self.updateWindow = updateWindow
        self.initGUI()

    def initGUI(self) -> None:
        self.label_icon = QLabel()
        self.label_icon.setPixmap(QPixmap(getAbsolutePath("assets", "trophy_looser.png")).scaled(128, 128))
        self.label_icon.setFixedSize(200, 200)
        self.label_icon.setAlignment(Qt.AlignCenter)
        self.button_back = getButton(self.buttonBackClicked, "Back", 100, 50)
        self.button_retry = getButton(self.buttonRetryClicked, "Retry", 100, 50)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.label_icon)
        layout.setAlignment(self.label_icon, Qt.AlignCenter)
        layout.addWidget(self.button_retry)
        layout.setAlignment(self.button_retry, Qt.AlignCenter)
        layout.addWidget(self.button_back)
        layout.setAlignment(self.button_back, Qt.AlignCenter)
        layout.addStretch()

        frame = QFrame()
        frame.setFrameShape(QFrame.Box)
        frame.setLineWidth(2)
        frame.setFixedSize(300, 300)
        frame.setLayout(layout)

        main_layout = QVBoxLayout()
        main_layout.addStretch()
        main_layout.addWidget(frame)
        main_layout.setAlignment(frame, Qt.AlignCenter)
        main_layout.addStretch()
        self.setLayout(main_layout)

    def buttonRetryClicked(self):
        self.updateWindow(MenuID.play)

    def buttonBackClicked(self):
        self.updateWindow(MenuID.home)
