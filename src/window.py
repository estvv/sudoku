from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.tools import *
from src.logger import *
from src.enums.enums import *
from src.gui.home import *
from src.gui.settings import *
from src.gui.play import *
from src.gui.pause import *

class Window(QMainWindow):
    gui_home: HomeGUI = None
    gui_settings: SettingsGUI = None
    gui_play: PlayGUI = None
    gui_pause: PauseGUI = None
    main_window: MenuID = MenuID.home

    def __init__(self) -> None:
        super().__init__()
        self.initGUI()
        self.initMenus()

    def initGUI(self) -> None:
        self.setWindowTitle("Sudoku")
        self.setWindowIcon(QIcon(getAbsolutePath("assets", "icon.png")))
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

    def initMenus(self) -> None:
        self.gui_home = HomeGUI(self.updateWindow, self.updateDifficulty)
        self.gui_settings = SettingsGUI()
        self.gui_play = PlayGUI(self.gui_home.difficulty)
        self.gui_pause = PauseGUI(self.updateWindow)
        self.current_menu = None
        self.updateWindow(MenuID.home)

    def updateWindow(self, menu_id: MenuID):
        if self.current_menu:
            self.layout.removeWidget(self.current_menu)
            self.current_menu.setParent(None)

        if menu_id == MenuID.home:
            logger.debug(f"Changing menu to Home")
            self.current_menu = self.gui_home
            self.main_window = MenuID.home
            self.gui_play = PlayGUI(self.gui_home.difficulty)
        elif menu_id == MenuID.settings:
            logger.debug(f"Changing menu to Settings")
            self.current_menu = self.gui_settings
            self.main_window = MenuID.settings
        elif menu_id == MenuID.play:
            logger.debug(f"Changing menu to Play")
            self.current_menu = self.gui_play
            self.main_window = MenuID.play
        elif menu_id == MenuID.pause:
            logger.debug(f"Changing menu to Pause")
            self.current_menu = self.gui_pause
            self.main_window = MenuID.pause
        elif menu_id == MenuID.close:
            logger.debug(f"Closing the window.")
            self.close()

        if self.current_menu:
            self.layout.addWidget(self.current_menu)
        else:
            logger.warning(f"Problem during the window's changement.")

    def updateDifficulty(self, button: QPushButton):
        self.gui_home.button_easy.setChecked(False)
        self.gui_home.button_medium.setChecked(False)
        self.gui_home.button_hard.setChecked(False)
        self.gui_home.button_impossible.setChecked(False)
        button.setChecked(True)

        if button.text() == "Easy":
            self.gui_home.difficulty = DifficultyID.easy
        elif button.text() == "Medium":
            self.gui_home.difficulty = DifficultyID.medium
        elif button.text() == "Hard":
            self.gui_home.difficulty = DifficultyID.hard
        else:
            self.gui_home.difficulty = DifficultyID.impossible
        self.gui_play.initGrid(self.gui_home.difficulty)

    def keyPressEvent(self, event) -> None:
        if self.main_window == MenuID.home:
            self.eventHome(event)
        elif self.main_window == MenuID.settings:
            self.eventSettings(event)
        elif self.main_window == MenuID.play:
            self.eventPlay(event)
        elif self.main_window == MenuID.pause:
            self.eventPause(event)
        else:
            super().keyPressEvent(event)

    def eventHome(self, event) -> None:
        if event.key() == Qt.Key_Escape:
            self.close()

    def eventSettings(self, event) -> None:
        if event.key() == Qt.Key_Escape:
            self.updateWindow(MenuID.home)

    def eventPlay(self, event) -> None:
        if event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
            for item in self.gui_play.table_sudoku.selectedItems():
                if item.isSelected():
                    item.setText("")
        if event.key() == Qt.Key_Escape:
            #self.gui_play.setGraphicsEffect(getBlurEffect(10))
            self.updateWindow(MenuID.pause)

    def eventPause(self, event) -> None:
        if event.key() == Qt.Key_Escape:
            #self.gui_play.setGraphicsEffect(None)
            self.updateWindow(MenuID.play)
