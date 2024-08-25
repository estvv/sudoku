from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.tools import *
from src.enums.enums import *

class MenuHome(QWidget):
    def __init__(self, switch_menu) -> None:
        super().__init__()
        self.initUI(switch_menu)

    def initUI(self, switch_menu):

        layout_difficulty = self.initDifficulty()

        layout_menu = self.initBasics(switch_menu)

        layout = QVBoxLayout()
        layout.addLayout(layout_difficulty)
        layout.addLayout(layout_menu)
        self.setLayout(layout)

    def initDifficulty(self) -> QHBoxLayout:
        layout_difficulty = QHBoxLayout()

        self.button_easy = getButton(lambda: self.buttonDifficultyClicked(self.button_easy), "Easy", [150, 40], [150, 40])
        self.button_easy.setToolTip("Easy difficulty.")
        self.button_easy.setStyleSheet("""
            QPushButton { color: green; }
            QPushButton:checked { color: black; background-color: #3E8E41; }""")
        self.button_easy.setCheckable(True)
        self.button_easy.setChecked(True)

        self.button_medium = getButton(lambda: self.buttonDifficultyClicked(self.button_medium), "Medium", [150, 40], [150, 40])
        self.button_medium.setToolTip("Medium difficulty.")
        self.button_medium.setStyleSheet("""
            QPushButton { color: yellow; }
            QPushButton:checked { color: black; background-color: #FFEB3B;  }""")
        self.button_medium.setGraphicsEffect(getBlurEffect())

        self.button_hard = getButton(lambda: self.buttonDifficultyClicked(self.button_hard), "Hard", [150, 40], [150, 40])
        self.button_hard.setToolTip("Hard difficulty.")
        self.button_hard.setStyleSheet("""
            QPushButton { color: orange; }
            QPushButton:checked { color: black; background-color: #FF9800;  }""")
        self.button_hard.setGraphicsEffect(getBlurEffect())

        self.button_impossible = getButton(lambda: self.buttonDifficultyClicked(self.button_impossible), "Impossible", [150, 40], [150, 40])
        self.button_impossible.setToolTip("Impossible difficulty.")
        self.button_impossible.setStyleSheet("""
            QPushButton { color: red; }
            QPushButton:checked { color: black; background-color: #C62828;  }""")
        self.button_impossible.setGraphicsEffect(getBlurEffect())

        layout_difficulty.addStretch()
        layout_difficulty.addWidget(self.button_easy)
        layout_difficulty.addWidget(self.button_medium)
        layout_difficulty.addWidget(self.button_hard)
        layout_difficulty.addWidget(self.button_impossible)
        layout_difficulty.addStretch()
        return layout_difficulty

    def initBasics(self, switch_menu) -> QVBoxLayout:
        layout_menu = QVBoxLayout()

        button_play = getButton(lambda: switch_menu(MenuID.play), "Play", [150, 40], None)
        button_play.setIcon(QIcon(getAbsolutePath("assets", "play.png")))
        button_play.setIconSize(QSize(32, 32))
        button_play.setToolTip("Play.")

        button_settings = getButton(lambda: None, "Settings", [150, 40], None)
        button_settings.setIcon(QIcon(getAbsolutePath("assets", "settings.png")))
        button_settings.setIconSize(QSize(32, 32))
        button_settings.setToolTip("Settings.")

        button_exit = getButton(lambda: switch_menu(MenuID.close), "Exit", [150, 40], None)
        button_exit.setIcon(QIcon(getAbsolutePath("assets", "exit.png")))
        button_exit.setIconSize(QSize(32, 32))
        button_exit.setToolTip("Exit.")

        layout_menu.addStretch()
        layout_menu.addWidget(button_play, alignment=Qt.AlignCenter)
        layout_menu.addWidget(button_settings, alignment=Qt.AlignCenter)
        layout_menu.addWidget(button_exit, alignment=Qt.AlignCenter)
        layout_menu.addStretch()
        return layout_menu

    def buttonDifficultyClicked(self, button: QPushButton) -> None:
        if not button.isCheckable():
            return
        self.button_easy.setChecked(False)
        self.button_medium.setChecked(False)
        self.button_hard.setChecked(False)
        self.button_impossible.setChecked(False)
        button.setChecked(True)

def getBlurEffect() -> QGraphicsBlurEffect:
    blur_effect = QGraphicsBlurEffect()
    blur_effect.setBlurRadius(5)
    return blur_effect
