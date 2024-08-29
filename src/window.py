from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.tools import *
from src.logger import *
from src.enums.enums import *
from src.gui.home import MenuHome
from src.gui.settings import MenuSettings
from src.gui.play import MenuPlay

class Window(QMainWindow):
    menu_home: MenuHome = None
    menu_settings: MenuSettings = None
    menu_play: MenuPlay = None
    main_window: MenuID = MenuID.home

    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        self.initMenus()

    def initUI(self) -> None:
        self.setWindowTitle("Sudoku")
        self.setWindowIcon(QIcon(getAbsolutePath("assets", "icon.png")))
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

    def initMenus(self) -> None:
        self.menu_home = MenuHome(self.updateWindow, self.updateDifficulty)
        self.menu_settings = MenuSettings()
        self.menu_play = MenuPlay()
        self.current_menu = None
        self.updateWindow(MenuID.home)

    def updateWindow(self, menu_id: MenuID):
        if self.current_menu:
            self.layout.removeWidget(self.current_menu)
            self.current_menu.setParent(None)

        if menu_id == MenuID.home:
            logger.debug(f"Changing menu to Home")
            self.current_menu = self.menu_home
            self.main_window = MenuID.home
        elif menu_id == MenuID.play:
            logger.debug(f"Changing menu to Play")
            self.current_menu = self.menu_play
            self.main_window = MenuID.play
        elif menu_id == MenuID.settings:
            logger.debug(f"Changing menu to Settings")
            self.current_menu = self.menu_settings
            self.main_window = MenuID.settings
        elif menu_id == MenuID.close:
            logger.debug(f"Closing the window.")
            self.close()

        if self.current_menu:
            self.layout.addWidget(self.current_menu)
        else:
            logger.warning(f"Problem during the window's changement.")

    def updateDifficulty(self, button: QPushButton):
        self.menu_home.button_easy.setChecked(False)
        self.menu_home.button_medium.setChecked(False)
        self.menu_home.button_hard.setChecked(False)
        self.menu_home.button_impossible.setChecked(False)
        button.setChecked(True)

        if button.text() == "Easy":
            self.menu_play.initGrid(DifficultyID.easy)
        elif button.text() == "Medium":
            self.menu_play.initGrid(DifficultyID.medium)
        elif button.text() == "Hard":
            self.menu_play.initGrid(DifficultyID.hard)
        else:
            self.menu_play.initGrid(DifficultyID.impossible)

    def keyPressEvent(self, event) -> None:
        if self.main_window == MenuID.home:
            self.eventHome(event)
        elif self.main_window == MenuID.settings:
            self.eventSettings(event)
        elif self.main_window == MenuID.play:
            self.eventPlay(event)
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
            for item in self.menu_play.table_sudoku.selectedItems():
                if item.isSelected():
                    item.setText("")
        if event.key() == Qt.Key_Escape:
            self.updateWindow(MenuID.home)
