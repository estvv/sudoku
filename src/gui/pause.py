from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.tools import *
from src.enums.enums import *

class PauseGUI(QWidget):
    def __init__(self, updateWindow) -> None:
        super().__init__()
        self.initUI(updateWindow)

    def initUI(self, updateWindow):
        self.button_back = getButton(lambda: updateWindow(MenuID.play), "Back", 120, 30)
        self.button_reset = getButton(lambda: updateWindow(MenuID.home), "Reset", 120, 30)

        layout = QVBoxLayout(self)
        layout.addStretch()
        layout.addWidget(self.button_back)
        layout.setAlignment(self.button_back, Qt.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(self.button_reset)
        layout.setAlignment(self.button_reset, Qt.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)
