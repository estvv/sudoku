import os
from typing import Callable, Tuple
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Window(QMainWindow):
    centralWidget: QWidget = None

    def __init__(self) -> None:
        super().__init__()
        self.initUI()

    def keyPressEvent(self, event) -> None:
        if self.centralWidget == self.widgetMenu:
            if event.key() == Qt.Key_Escape:
                self.close()
            else:
                super().keyPressEvent(event)
        else:
            if event.key() == Qt.Key_Escape:
                #self.setCentralWidget(self.widgetMenu)
                self.centralWidget = self.widgetMenu
            else:
                super().keyPressEvent(event)

    def initUI(self) -> None:
        self.setWindowTitle("Sudoku")
        self.setWindowIcon(QIcon(os.path.abspath(os.path.join("assets", "icon.svg"))))
        self.widgetMenu = self.initMenu()
        self.widgetPlay = self.initPlay()
        self.centralWidget = self.widgetMenu
        self.setCentralWidget(self.widgetMenu)

    def getButton(self, func: Callable[[], None], title: str = None, min_size: Tuple[int, int] = None, max_size: Tuple[int, int] = None) -> QPushButton:
        button = QPushButton(title)
        if min_size:
            button.setMinimumSize(min_size[0], min_size[1])
        if max_size:
            button.setMaximumSize(max_size[0], max_size[1])
        button.clicked.connect(func)
        return button

    def initMenu(self) -> QWidget:
        widgetMenu = QWidget()

        buttonPlay     = self.getButton(self.buttonPlayClicked, "Play", [150, 40], None)
        buttonSettings = self.getButton(self.buttonSettingsClicked, "Settings", [150, 40], None)
        buttonExit     = self.getButton(self.buttonExitClicked, "Exit", [150, 40], None)

        layoutMenu = QVBoxLayout()
        layoutMenu.addStretch()
        layoutMenu.addWidget(buttonPlay, alignment=Qt.AlignCenter)
        layoutMenu.addWidget(buttonSettings, alignment=Qt.AlignCenter)
        layoutMenu.addWidget(buttonExit, alignment=Qt.AlignCenter)
        layoutMenu.addStretch()
        widgetMenu.setLayout(layoutMenu)
        return widgetMenu

    def buttonPlayClicked(self) -> None:
        self.setCentralWidget(self.widgetPlay)
        self.centralWidget = self.widgetPlay

    def buttonSettingsClicked(self) -> None:
        return

    def buttonExitClicked(self) -> None:
        self.close()

    def initPlay(self) -> QWidget:
        widgetPlay = QWidget()

        font: QFont = QFont()
        font.setPointSize(30)
        font.setFamily("Arial")

        tableSudoku = QTableWidget()
        tableSudoku.setFixedSize(900, 600)
        tableSudoku.setRowCount(3)
        tableSudoku.setColumnCount(3)
        tableSudoku.setFont(font)

        for i in range(3):
            for j in range(3):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(font)
                item.data(Qt.BackgroundColorRole)
                tableSudoku.setItem(i, j, item)

        tableSudoku.verticalHeader().setVisible(False)
        tableSudoku.horizontalHeader().setVisible(False)

        tableSudoku.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tableSudoku.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #tableSudoku.setEditTriggers(QAbstractItemView.EditKeyPressed)

        for i in range(3):
            tableSudoku.setColumnWidth(i, 300)
            tableSudoku.setRowHeight(i, 200)

        layoutPlay = QHBoxLayout()
        layoutPlay.addWidget(tableSudoku)
        widgetPlay.setLayout(layoutPlay)

        return widgetPlay
