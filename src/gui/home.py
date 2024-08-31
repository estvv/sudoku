from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.tools import *
from src.enums.enums import *

class HomeGUI(QWidget):
    difficulty: DifficultyID = DifficultyID.easy

    def __init__(self, updateMenu, updateDifficulty) -> None:
        super().__init__()
        self.initGUI(updateMenu, updateDifficulty)

    def initGUI(self, updateMenu, updateDifficulty):
        layout_difficulty = self.initDifficulty(updateDifficulty)
        layout_menu = self.initBasics(updateMenu)

        layout = QVBoxLayout()
        layout.addLayout(layout_difficulty)
        layout.addLayout(layout_menu)
        self.setLayout(layout)

    def initDifficulty(self, updateDifficulty) -> QHBoxLayout:
        layout_difficulty = QHBoxLayout()

        self.button_easy = getButton(lambda: updateDifficulty(self.button_easy), "Easy", 150, 40)
        self.button_easy.setToolTip("Easy difficulty.")
        self.button_easy.setStyleSheet("QPushButton { color: green; } QPushButton:checked { color: black; background-color: #3E8E41; }")
        self.button_easy.setCheckable(True)
        self.button_easy.setChecked(True)

        self.button_medium = getButton(lambda: updateDifficulty(self.button_medium), "Medium", 150, 40)
        self.button_medium.setToolTip("Medium difficulty.")
        self.button_medium.setStyleSheet("QPushButton { color: yellow; } QPushButton:checked { color: black; background-color: #FFEB3B;  }")
        self.button_medium.setCheckable(True)
        self.button_medium.setChecked(False)

        self.button_hard = getButton(lambda: updateDifficulty(self.button_hard), "Hard", 150, 40)
        self.button_hard.setToolTip("Hard difficulty.")
        self.button_hard.setStyleSheet("QPushButton { color: orange; } QPushButton:checked { color: black; background-color: #FF9800;  }")
        self.button_hard.setCheckable(True)
        self.button_hard.setChecked(False)

        self.button_impossible = getButton(lambda: updateDifficulty(self.button_impossible), "Impossible", 150, 40)
        self.button_impossible.setToolTip("Impossible difficulty.")
        self.button_impossible.setStyleSheet("QPushButton { color: red; } QPushButton:checked { color: black; background-color: #C62828;  }")
        self.button_impossible.setCheckable(True)
        self.button_impossible.setChecked(False)

        layout_difficulty.addStretch()
        layout_difficulty.addWidget(self.button_easy)
        layout_difficulty.addWidget(self.button_medium)
        layout_difficulty.addWidget(self.button_hard)
        layout_difficulty.addWidget(self.button_impossible)
        layout_difficulty.addStretch()
        return layout_difficulty

    def initBasics(self, updateMenu) -> QVBoxLayout:
        layout_menu = QVBoxLayout()

        button_play = getButton(lambda: updateMenu(MenuID.play), " Play", 150, 40)
        button_play.setIcon(QIcon(getAbsolutePath("assets", "valid.png")))
        button_play.setIconSize(QSize(32, 32))
        button_play.setToolTip("Play.")

        button_settings = getButton(lambda: updateMenu(MenuID.settings), " Settings", 150, 40)
        button_settings.setIcon(QIcon(getAbsolutePath("assets", "settings.png")))
        button_settings.setIconSize(QSize(32, 32))
        button_settings.setToolTip("Settings.")

        button_exit = getButton(lambda: updateMenu(MenuID.close), " Exit", 150, 40)
        button_exit.setIcon(QIcon(getAbsolutePath("assets", "not_valid.png")))
        button_exit.setIconSize(QSize(32, 32))
        button_exit.setToolTip("Exit.")

        layout_menu.addStretch()
        layout_menu.addWidget(button_play, alignment=Qt.AlignCenter)
        layout_menu.addWidget(button_settings, alignment=Qt.AlignCenter)
        layout_menu.addWidget(button_exit, alignment=Qt.AlignCenter)
        layout_menu.addStretch()
        return layout_menu
