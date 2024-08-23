import os
import logging
from src.logger import *
from typing import Callable, Tuple
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class SudokuBorder(QStyledItemDelegate):
    def paint(self, painter, option, index):
        super().paint(painter, option, index)

        if (index.column() + 1) % 3 == 0 and (index.column() + 1) != 9:
            pen = QPen(Qt.gray, 2)
            painter.setPen(pen)
            painter.drawLine(option.rect.topRight(), option.rect.bottomRight())
        if (index.row() + 1) % 3 == 0 and (index.row() + 1) != 9:
            pen = QPen(Qt.gray, 2)
            painter.setPen(pen)
            painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())

class Window(QMainWindow):
    logger = None
    widgetMenu: QWidget = None
    widgetPlay: QWidget = None
    font: QFont = None

    def __init__(self) -> None:
        super().__init__()
        self.logger = setLogger()
        self.font = QFont("Arial", 12)
        self.initUI()

    def keyPressEvent(self, event) -> None:
        self.logger.info(f"The {event.text()} key is pressed")
        if self.centralWidget() == self.widgetMenu:
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
                    item.setText(event.text())

    def initUI(self) -> None:
        self.setWindowTitle("Sudoku")
        self.setWindowIcon(QIcon(getAbsolutePath("assets", "icon.png")))
        self.widgetMenu = self.initMenu()
        self.widgetPlay = self.initPlay()
        self.setCentralWidget(self.widgetMenu)

    def getButton(self, func: Callable[[], None], title: str = None, min_size: Tuple[int, int] = None, max_size: Tuple[int, int] = None) -> QPushButton:
        button = QPushButton(title)
        if min_size:
            button.setMinimumSize(min_size[0], min_size[1])
        if max_size:
            button.setMaximumSize(max_size[0], max_size[1])
        button.clicked.connect(func)
        return button

    def getSelfButton(self, func: Callable[[QPushButton], None], title: str = None, min_size: Tuple[int, int] = None, max_size: Tuple[int, int] = None) -> QPushButton:
        button = QPushButton(title)
        if min_size:
            button.setMinimumSize(min_size[0], min_size[1])
        if max_size:
            button.setMaximumSize(max_size[0], max_size[1])
        button.clicked.connect(lambda: func(button))
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

    def initPlay(self) -> QWidget:
        widgetPlay = QWidget()

        self.buttonBack = self.getButton(self.buttonBackClicked, "<-")
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.buttonBack)
        topLayout.addStretch()

        toolsLayout = self.initTools()
        self.initSudokuTable()
        numbersLayout = self.initNumbers()

        layoutPlay = QVBoxLayout()
        layoutPlay.addLayout(topLayout)
        layoutPlay.addWidget(self.tableSudoku)
        layoutPlay.setAlignment(self.tableSudoku, Qt.AlignHCenter)
        layoutPlay.addLayout(toolsLayout)
        layoutPlay.setAlignment(toolsLayout, Qt.AlignHCenter)
        layoutPlay.addLayout(numbersLayout)
        layoutPlay.setAlignment(numbersLayout, Qt.AlignHCenter)
        widgetPlay.setLayout(layoutPlay)

        return widgetPlay

    def initTools(self) -> QHBoxLayout:
        toolsLayout = QHBoxLayout()
        self.buttonErase = self.getButton(self.buttonEraseClicked, "", [100, 50])
        self.buttonErase.setIcon(QIcon(getAbsolutePath("assets", "eraser.png")))
        self.buttonErase.setIconSize(QSize(32, 32))
        self.buttonErase.setToolTip("Click to erase a box.")

        self.buttonPen = self.getButton(self.buttonPenClicked, "", [100, 50])
        self.buttonPen.setIcon(QIcon(getAbsolutePath("assets", "pen.png")))
        self.buttonPen.setIconSize(QSize(32, 32))
        self.buttonPen.setCheckable(True)
        self.buttonPen.setToolTip("Click to enable comment.")

        self.buttonHint = self.getButton(self.buttonNumberClicked, "  0 / 3", [100, 50])
        self.buttonHint.setIcon(QIcon(getAbsolutePath("assets", "hint.png")))
        self.buttonHint.setIconSize(QSize(32, 32))

        toolsLayout.addWidget(self.buttonErase)
        toolsLayout.addSpacing(40)
        toolsLayout.addWidget(self.buttonPen)
        toolsLayout.addSpacing(40)
        toolsLayout.addWidget(self.buttonHint)
        return toolsLayout

    def initSudokuTable(self) -> None:
        self.tableSudoku = QTableWidget(9, 9)
        self.tableSudoku.setFixedSize(900, 600)
        self.tableSudoku.setFont(self.font)
        self.tableSudoku.setItemDelegate(SudokuBorder())
        self.tableSudoku.horizontalHeader().setVisible(False)
        self.tableSudoku.verticalHeader().setVisible(False)
        self.tableSudoku.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableSudoku.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i in range(9):
            for j in range(9):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(self.font)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.tableSudoku.setItem(i, j, item)

    def initNumbers(self) -> QHBoxLayout:
        numbersLayout = QHBoxLayout()
        self.buttonsNumber: list[QPushButton] = []
        for i in range(1, 10):
            self.buttonsNumber.append(self.getSelfButton(self.buttonNumberClicked, str(i), [95, 50]))
        for i in range(len(self.buttonsNumber)):
            numbersLayout.addWidget(self.buttonsNumber[i])
        return numbersLayout

    def buttonPlayClicked(self) -> None:
        self.widgetPlay = self.initPlay()
        self.setCentralWidget(self.widgetPlay)

    def buttonSettingsClicked(self) -> None:
        return

    def buttonExitClicked(self) -> None:
        self.close()

    def buttonBackClicked(self) -> None:
        self.widgetMenu = self.initMenu()
        self.setCentralWidget(self.widgetMenu)

    def onItemChanged(self, item: QTableWidgetItem) -> None:
        if len(item.text()) > 1:
            item.setText(item.text()[:1])

    def buttonEraseClicked(self) -> None:
        for item in self.tableSudoku.selectedItems():
            if item.isSelected():
                item.setText("")

    def buttonPenClicked(self) -> None:
        if self.buttonPen.isChecked():
            self.buttonPen.setToolTip("Click to enable writing.")
        else:
            self.buttonPen.setToolTip("Click to enable comment.")

    def buttonHintClicked(self) -> None:
        state: QTableWidget = None
        for item in self.tableSudoku.selectedItems():
            if item.isSelected():
                state = item
                break
        if not state:
            return

    def buttonNumberClicked(self, button: QPushButton) -> None:
        for item in self.tableSudoku.selectedItems():
            if item.isSelected() and self.buttonPen.isChecked():
                item.setForeground(QColor("red"))
                item.setText(button.text())
            else:
                item.setText(button.text())

def getAbsolutePath(folder: str, filename: str) -> None:
    return os.path.abspath(os.path.join(folder, filename))
