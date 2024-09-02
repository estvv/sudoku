from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src import *
from src.gui import *

class Window(QMainWindow):
    gui_home: HomeGUI = None
    gui_settings: SettingsGUI = None
    gui_play: PlayGUI = None
    gui_pause: PauseGUI = None
    main_window: MenuID = MenuID.home
    prev_window: MenuID = MenuID.close

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
        self.gui_play = PlayGUI(self.updateWindow, self.gui_home.difficulty)
        self.gui_pause = PauseGUI(self.updateWindow)
        self.gui_win = WinGUI(self.updateWindow)
        self.gui_loose = LooseGUI(self.updateWindow)
        self.current_menu = None
        self.updateWindow(MenuID.home)

    def updateWindow(self, menu_id: MenuID):
        if self.current_menu:
            self.layout.removeWidget(self.current_menu)
            self.current_menu.setParent(None)

        self.prev_window = self.main_window
        if menu_id == MenuID.home:
            logger.debug(f"Changing menu to Home")
            self.current_menu = self.gui_home
            self.main_window = MenuID.home
            self.gui_play = PlayGUI(self.updateWindow, self.gui_home.difficulty, self.gui_play.theme)
        elif menu_id == MenuID.settings:
            logger.debug(f"Changing menu to Settings")
            self.current_menu = self.gui_settings
            self.main_window = MenuID.settings
        elif menu_id == MenuID.play:
            logger.debug(f"Changing menu to Play")
            self.main_window = MenuID.play
            if self.prev_window != MenuID.pause:
                self.gui_play = PlayGUI(self.updateWindow, self.gui_home.difficulty, self.gui_play.theme)
            self.current_menu = self.gui_play
        elif menu_id == MenuID.pause:
            logger.debug(f"Changing menu to Pause")
            self.current_menu = self.gui_pause
            self.main_window = MenuID.pause
        elif menu_id == MenuID.loose:
            logger.debug(f"You loose.")
            self.current_menu = self.gui_loose
            self.main_window = MenuID.loose
        elif menu_id == MenuID.win:
            logger.debug(f"You win.")
            self.current_menu = self.gui_win
            self.main_window = MenuID.win
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
            self.updateWindow(self.prev_window)

    def eventPlay(self, event) -> None:
        if event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
            for item in self.gui_play.table_sudoku.selectedItems():
                if item.isSelected():
                    item.setText("")
        if event.key() == Qt.Key_Escape:
            self.updateWindow(MenuID.pause)

    def eventPause(self, event) -> None:
        if event.key() == Qt.Key_Escape:
            self.updateWindow(MenuID.play)
