from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.tools import *
from src.enums.enums import *

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

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setAlignment(Qt.AlignCenter)
        editor.setMaxLength(1)
        editor.setValidator(QIntValidator(1, 9, editor))
        return editor

class MenuPlay(QWidget):
    widgetMenuPlay: QWidget = None
    font: QFont = None

    def __init__(self, switch_menu) -> None:
        super().__init__()
        self.switch_menu = switch_menu
        self.font = QFont("Arial", 12)
        self.initUI()

    def initUI(self):
        self.buttonBack = getButton(lambda: self.switch_menu(MenuID.home), "<")
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
        self.setLayout(layoutPlay)

    def initTools(self) -> QHBoxLayout:
        toolsLayout = QHBoxLayout()
        self.buttonErase = getButton(self.buttonEraseClicked, "", [100, 50])
        self.buttonErase.setIcon(QIcon(getAbsolutePath("assets", "eraser.png")))
        self.buttonErase.setIconSize(QSize(32, 32))
        self.buttonErase.setToolTip("Click to erase a box.")

        self.buttonPen = getButton(self.buttonPenClicked, "", [100, 50])
        self.buttonPen.setIcon(QIcon(getAbsolutePath("assets", "pen.png")))
        self.buttonPen.setIconSize(QSize(32, 32))
        self.buttonPen.setCheckable(True)
        self.buttonPen.setToolTip("Click to enable comment.")

        self.buttonHint = getButton(self.buttonNumberClicked, "  0 / 3", [100, 50])
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
        self.tableSudoku.setSelectionMode(QAbstractItemView.SingleSelection)

        for i in range(9):
            for j in range(9):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(self.font)
                self.tableSudoku.setItem(i, j, item)
        self.blackTheme()

    def blackTheme(self):
        default_bg_color = QColor("black")
        active_bg_color = QColor("#1e1e1e")

        for i in range(9):
            for j in range(9):
                item = self.tableSudoku.item(i, j)
                item.setBackground(default_bg_color)
                item.setForeground(QColor("white"))

        # Pour l'état activé (focus) des cellules
        self.tableSudoku.setStyleSheet(f"""
            QTableWidget::item:selected {{
                background-color: {active_bg_color.name()};
                border: 1px solid {active_bg_color.darker().name()};
            }}
        """)

    def whiteTheme(self):
        default_bg_color = QColor("white")  # Couleur de fond par défaut
        active_bg_color =  QColor("#f0f0f0")  # Couleur pour les cellules activées

        for i in range(9):
            for j in range(9):
                item = self.tableSudoku.item(i, j)
                item.setBackground(default_bg_color)
                item.setForeground(QColor("black"))

        self.tableSudoku.setStyleSheet(f"""
            QTableWidget::item:selected {{
                background-color: {active_bg_color.name()};
                border: 1px solid {active_bg_color.darker().name()};
            }}
        """)

    def initNumbers(self) -> QHBoxLayout:
        numbersLayout = QHBoxLayout()
        self.buttonsNumber: list[QPushButton] = []
        for i in range(1, 10):
            self.buttonsNumber.append(getSelfButton(self.buttonNumberClicked, str(i), [95, 50]))
        for i in range(len(self.buttonsNumber)):
            numbersLayout.addWidget(self.buttonsNumber[i])
        return numbersLayout

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
