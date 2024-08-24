from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.tools import *
from src.logger import *
from src.enums.enums import *
from src.menus.home import MenuHome
from src.menus.play import MenuPlay

class Window(QMainWindow):
    logger = None
    menuHome: MenuHome = None
    menuPlay: MenuPlay = None
    widgetHome: QWidget = None
    widgetPlay: QWidget = None

    def __init__(self) -> None:
        super().__init__()
        self.logger = setLogger()
        self.initUI()
        self.initMenus()

    def initUI(self) -> None:
        self.setWindowTitle("Sudoku")
        self.setWindowIcon(QIcon(getAbsolutePath("assets", "icon.png")))
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

    def initMenus(self) -> None:
        self.menuHome = MenuHome(self.change_window)
        self.menuPlay = MenuPlay(self.change_window)
        self.current_menu = None
        self.change_window(MenuID.home)

    def change_window(self, menu_id: MenuID):
        if self.current_menu:
            self.layout.removeWidget(self.current_menu)
            self.current_menu.setParent(None)

        if menu_id == MenuID.home:
            self.logger.debug(f"Changing menu -> Home")
            self.current_menu = self.menuHome
        elif menu_id == MenuID.play:
            self.logger.debug(f"Changing menu -> Play")
            self.current_menu = self.menuPlay
        else:
            self.logger.debug(f"Closing the window.")
            self.close()

        if self.current_menu:
            self.layout.addWidget(self.current_menu)
        else:
            self.logger.warning(f"Problem during the window's changement.")

    def keyPressEvent(self, event) -> None:
        self.logger.info(f"The {event.text()} key is pressed")
        if self.centralWidget() == self.widgetHome:
            self.eventMenu(event)
        elif self.centralWidget() == self.widgetPlay:
            self.eventPlay(event)
        else:
            super().keyPressEvent(event)

    def eventMenu(self, event) -> None:
        if event.key() == Qt.Key_Escape:
            self.close()

    def eventPlay(self, event) -> None:
        if event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
            for item in self.tableSudoku.selectedItems():
                if item.isSelected():
                    item.setText("")
        elif event.text().isnumeric():
            for item in self.tableSudoku.selectedItems():
                if item.isSelected():
                    item.setText("")
                    item.setText(event.text())
