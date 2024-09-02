from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src import *

class PauseGUI(QWidget):
    def __init__(self, updateWindow) -> None:
        super().__init__()
        self.initUI(updateWindow)

    def initUI(self, updateWindow):
        self.label_icon_pause = QLabel()
        self.label_icon_pause.setPixmap(QPixmap(getAbsolutePath("assets", "pause.png")).scaled(32, 32))
        self.label_icon_pause.setFixedSize(100, 50)
        self.label_icon_pause.setAlignment(Qt.AlignCenter)
        self.button_back = getButton(lambda: updateWindow(MenuID.play), "Back", 120, 30)
        self.button_settings = getButton(lambda: updateWindow(MenuID.settings), "Settings", 120, 30)
        self.button_reset = getButton(lambda: updateWindow(MenuID.home), "Reset", 120, 30)

        layout = QVBoxLayout(self)
        layout.addStretch()
        layout.addWidget(self.label_icon_pause)
        layout.setAlignment(self.label_icon_pause, Qt.AlignCenter)
        layout.addWidget(self.button_back)
        layout.setAlignment(self.button_back, Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.button_settings)
        layout.setAlignment(self.button_settings, Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.button_reset)
        layout.setAlignment(self.button_reset, Qt.AlignCenter)
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
