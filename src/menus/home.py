from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.tools import *
from src.enums.enums import *

class MenuHome(QWidget):
    widgetMenuHome: QWidget = None

    def __init__(self, switch_menu) -> None:
        super().__init__()
        self.switch_menu = switch_menu
        self.initUI()

    def initUI(self):
        self.buttonPlay = getButton(lambda: self.switch_menu(MenuID.play), "Play", [150, 40], None)
        self.buttonPlay.setIcon(QIcon(getAbsolutePath("assets", "play.png")))
        self.buttonPlay.setIconSize(QSize(32, 32))
        self.buttonPlay.setToolTip("Play.")

        self.buttonSettings = getButton(lambda: None, "Settings", [150, 40], None)
        self.buttonSettings.setIcon(QIcon(getAbsolutePath("assets", "settings.png")))
        self.buttonSettings.setIconSize(QSize(32, 32))
        self.buttonSettings.setToolTip("Settings.")

        self.buttonExit = getButton(lambda: self.switch_menu(MenuID.close), "Exit", [150, 40], None)
        self.buttonExit.setIcon(QIcon(getAbsolutePath("assets", "exit.png")))
        self.buttonExit.setIconSize(QSize(32, 32))
        self.buttonExit.setToolTip("Exit.")

        layoutMenu = QVBoxLayout()
        layoutMenu.addStretch()
        layoutMenu.addWidget(self.buttonPlay, alignment=Qt.AlignCenter)
        layoutMenu.addWidget(self.buttonSettings, alignment=Qt.AlignCenter)
        layoutMenu.addWidget(self.buttonExit, alignment=Qt.AlignCenter)
        layoutMenu.addStretch()
        self.setLayout(layoutMenu)
