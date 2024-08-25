from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.tools import *
from src.logger import *
from src.enums.enums import *
from src.menus.home import MenuHome
from src.menus.play import MenuPlay

class Window(QMainWindow):
    menu_play: MenuPlay = None
    widget_play: QWidget = None
    menu_home: MenuHome = None
    widget_home: QWidget = None
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
        self.menu_home = MenuHome(self.change_window)
        self.menu_play = MenuPlay(self.change_window)
        self.current_menu = None
        self.change_window(MenuID.home)

    def change_window(self, menu_id: MenuID):
        if self.current_menu:
            self.layout.removeWidget(self.current_menu)
            self.current_menu.setParent(None)

        if menu_id == MenuID.home:
            logger.debug(f"Changing menu -> Home")
            self.current_menu = self.menu_home
            self.main_window = MenuID.home
        elif menu_id == MenuID.play:
            logger.debug(f"Changing menu -> Play")
            self.current_menu = self.menu_play
            self.main_window = MenuID.play
        else:
            logger.debug(f"Closing the window.")
            self.close()

        if self.current_menu:
            self.layout.addWidget(self.current_menu)
        else:
            logger.warning(f"Problem during the window's changement.")

    def keyPressEvent(self, event) -> None:
        if self.main_window == MenuID.home:
            self.eventMenu(event)
        elif self.main_window == MenuID.play:
            self.eventPlay(event)
        else:
            super().keyPressEvent(event)

    def eventMenu(self, event) -> None:
        if event.key() == Qt.Key_Escape:
            self.close()

    def eventPlay(self, event) -> None:
        if event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
            for item in self.menu_play.table_sudoku.selectedItems():
                if item.isSelected():
                    item.setText("")
