import qdarkstyle
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.logger import *
from src.tools import *
from src.enums.enums import *
from src.objects.buttons.slicing_button import *

darkColors: dict[str, QColor] = {
    "item-foreground": QColor("white"),
    "item-background": QColor("black"),
    "item-background_selected": QColor(30, 30, 30),
    "item-premade": QColor(65,105,225),
    "item-made": QColor("yellow"),
    "item-false": QColor("red"),
    "item-comment": QColor(128, 128, 128),
    "item-big_border": QColor(220, 220, 220),
    "item-little_border": QColor(55, 65, 79)
}

whiteColors: dict[str, QColor] = {
    "item-foreground": QColor("black"),
    "item-background": QColor("white"),
    "item-background_selected": QColor(240, 240, 240),
    "item-premade": QColor(65, 105, 225),
    "item-made": QColor("yellow"),
    "item-false": QColor("red"),
    "item-comment": QColor(128, 128, 128),
    "item-big_border": QColor(150, 150, 150),
    "item-little_border": QColor(192, 196, 200)
}

class DelegateSudokuTable(QStyledItemDelegate):
    def __init__(self, button_pen: QPushButton, colors: dict[str, QColor], parent = None) -> None:
        super().__init__(parent)
        self.button_pen = button_pen
        self.colors = colors
        self.previous_text = ""
        self.recursion_error = False

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        super().paint(painter, option, index)

        lil_borders = QPen(QColor(self.colors["item-little_border"]), 3)
        big_borders = QPen(QColor(self.colors["item-big_border"]), 2)

        # draw lil borders
        painter.setPen(lil_borders)
        if index.column() == 0:
            painter.drawLine(option.rect.topLeft(), option.rect.bottomLeft())
        if (index.column() + 1) % 9 == 0:
            painter.drawLine(option.rect.topRight(), option.rect.bottomRight())
        if index.row() == 0:
            painter.drawLine(option.rect.topLeft(), option.rect.topRight())
        if (index.row() + 1) % 9 == 0:
            painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())

        # draw big borders
        painter.setPen(big_borders)
        if (index.column() + 1) % 3 == 0 and (index.column() + 1) != 9:
            painter.drawLine(option.rect.topRight(), option.rect.bottomRight())
        if (index.row() + 1) % 3 == 0 and (index.row() + 1) != 9:
            painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())

    def createEditor(self, parent, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        editor = QLineEdit(parent)
        editor.setAlignment(Qt.AlignCenter)
        if self.button_pen.isChecked():
            editor.setMaxLength(9)
            editor.setValidator(QRegExpValidator(QRegExp("^[1-9]{1,9}$"), editor))
        else:
            editor.setMaxLength(1)
            editor.setValidator(QRegExpValidator(QRegExp("[1-9]"), editor))
        editor.textChanged.connect(self.onTextChanged)
        return editor

    def onTextChanged(self, text: str) -> None:
        if self.recursion_error:
            return
        editor = self.sender()
        if editor:
            if self.button_pen.isChecked():
                if self.previous_text:
                    text += self.previous_text
                    self.previous_text = ""
                sorted_text = getCleanedString(text)
                self.recursion_error = True
                editor.setText(sorted_text)
                self.recursion_error = False
            else:
                self.recursion_error = True
                editor.setText(text)
                self.recursion_error = False
                event = QKeyEvent(QEvent.KeyPress, Qt.Key_Return, Qt.NoModifier)
                QApplication.sendEvent(editor, event)

    def setEditorData(self, editor : QWidget, index: QModelIndex) -> None:
        text = index.data(Qt.DisplayRole)
        if text is None:
            text = ""
        editor.setText(text)
        self.previous_text = text

class MenuPlay(QWidget):
    font: QFont = None
    colors: dict = darkColors
    theme: ThemeID = ThemeID.dark
    grid: list[list[int]] = None
    grid_solved: list[list[int]] = None
    errors: int = 0

    def __init__(self) -> None:
        super().__init__()
        self.font = QFont("Arial", 12)
        self.initUI()

    def initUI(self) -> None:
        layout_errors = self.initErrors()

        self.button_theme = SlicingButton("", 200, 30, self.colors["item-foreground"], self.colors["item-background"], self)
        self.button_theme.animation.finished.connect(self.buttonThemeAnimationFinished)
        layout_top = QHBoxLayout()
        layout_top.addStretch()
        layout_top.addWidget(self.button_theme)
        layout_top.addStretch()

        layout_tools = self.initTools()
        self.initSudokuTable()
        layout_numbers = self.initNumbers()

        layout_play = QVBoxLayout()
        layout_play.addLayout(layout_errors)
        layout_play.setAlignment(layout_errors, Qt.AlignHCenter)
        layout_play.addLayout(layout_top)
        layout_play.addWidget(self.table_sudoku)
        layout_play.setAlignment(self.table_sudoku, Qt.AlignHCenter)
        layout_play.addLayout(layout_tools)
        layout_play.setAlignment(layout_tools, Qt.AlignHCenter)
        layout_play.addLayout(layout_numbers)
        layout_play.setAlignment(layout_numbers, Qt.AlignHCenter)
        self.setLayout(layout_play)

    def initErrors(self) -> QHBoxLayout:
        layout_errors = QHBoxLayout()
        self.label_errors: list[QLabel] = []
        for i in range(3):
            tmp = QLabel()
            tmp.setFixedSize(50, 50)
            tmp.setAlignment(Qt.AlignCenter)
            tmp.setPixmap(QPixmap(getAbsolutePath("assets", "heart.png")).scaled(32, 32))
            self.label_errors.append(tmp)

        self.label_errors.reverse()
        layout_errors.addStretch()
        layout_errors.addWidget(self.label_errors[0])
        layout_errors.addWidget(self.label_errors[1])
        layout_errors.addWidget(self.label_errors[2])
        layout_errors.addStretch()
        return layout_errors

    def initTools(self) -> QHBoxLayout:
        layout_tools = QHBoxLayout()
        self.button_erase = getButton(self.buttonEraseClicked, "", 100, 50)
        self.button_erase.setIcon(QIcon(getAbsolutePath("assets", "eraser.png")))
        self.button_erase.setIconSize(QSize(32, 32))
        self.button_erase.setToolTip("Click to erase a box.")

        self.button_pen = getButton(self.buttonPenClicked, "", 100, 50)
        self.button_pen.setIcon(QIcon(getAbsolutePath("assets", "pen.png")))
        self.button_pen.setIconSize(QSize(32, 32))
        self.button_pen.setCheckable(True)
        self.button_pen.setToolTip("Click to enable comment.")

        self.button_hint = getButton(lambda: None, "  0 / 3", 100, 50)
        self.button_hint.setIcon(QIcon(getAbsolutePath("assets", "hint.png")))
        self.button_hint.setIconSize(QSize(32, 32))

        layout_tools.addWidget(self.button_erase)
        layout_tools.addSpacing(40)
        layout_tools.addWidget(self.button_pen)
        layout_tools.addSpacing(40)
        layout_tools.addWidget(self.button_hint)
        return layout_tools

    def initSudokuTable(self) -> None:
        self.table_sudoku = QTableWidget(9, 9)
        self.table_sudoku.setFixedSize(900, 600)
        self.table_sudoku.setFont(self.font)
        self.table_sudoku.setItemDelegate(DelegateSudokuTable(self.button_pen, self.colors))
        self.table_sudoku.horizontalHeader().setVisible(False)
        self.table_sudoku.verticalHeader().setVisible(False)
        self.table_sudoku.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_sudoku.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_sudoku.setSelectionMode(QAbstractItemView.SingleSelection)

        self.initGrid(DifficultyID.easy)
        self.table_sudoku.itemClicked.connect(self.onItemClicked)

    def initGrid(self, difficulty) -> None:
        self.grid, self.grid_solved = create_grid(difficulty)
        self.table_sudoku.clear()

        for i in range(9):
            for j in range(9):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(self.font)
                if self.grid[i][j]:
                    item.setText(str(self.grid[i][j]))
                self.table_sudoku.setItem(i, j, item)

        self.updateTheme()

        for i in range(9):
            for j in range(9):
                item = self.table_sudoku.item(i, j)
                if self.grid[i][j]:
                    item.setForeground(self.colors["item-premade"])
                    item.setFlags(Qt.ItemIsEnabled)

    def initNumbers(self) -> QHBoxLayout:
        layout_numbers = QHBoxLayout()
        self.buttonsNumber: list[QPushButton] = []
        for i in range(1, 10):
            self.buttonsNumber.append(getSelfButton(self.buttonNumberClicked, str(i), 95, 50))
        for i in range(len(self.buttonsNumber)):
            layout_numbers.addWidget(self.buttonsNumber[i])
        return layout_numbers

    def onItemClicked(self) -> None:
        for item in self.table_sudoku.selectedItems():
            if self.button_pen.isChecked():
                item.setForeground(self.colors["item-comment"])
            else:
                item.setForeground(self.colors["item-foreground"])

    def buttonThemeAnimationFinished(self) -> None:
        app = QApplication.instance()

        if self.button_theme.slider_pos > 0:
            app.setStyleSheet(qdarkstyle.load_stylesheet(palette=qdarkstyle.LightPalette))
            logger.info("Light")
            self.button_theme.setText("")
            self.colors = whiteColors
            self.updateTheme()
            self.theme = ThemeID.light
        else:
            app.setStyleSheet(qdarkstyle.load_stylesheet(palette=qdarkstyle.DarkPalette))
            logger.info("Dark")
            self.button_theme.setText("")
            self.colors = darkColors
            self.updateTheme()
            self.theme = ThemeID.dark

    def updateTheme(self) -> None:
        self.table_sudoku.setItemDelegate(DelegateSudokuTable(self.button_pen, self.colors))
        for i in range(9):
            for j in range(9):
                item = self.table_sudoku.item(i, j)
                item.setBackground(self.colors["item-background"])
                if item.foreground().color() == self.colors["item-background"]:
                    item.setForeground(self.colors["item-foreground"])

        self.table_sudoku.setStyleSheet(f"""
            QTableWidget::item:selected {{
                background-color: {self.colors["item-background_selected"].name()};
            }}
            QTableWidget {{
                border: none;
            }}
        """)

    def buttonEraseClicked(self) -> None:
        for item in self.table_sudoku.selectedItems():
            item.setText("")

    def buttonPenClicked(self) -> None:
        for item in self.table_sudoku.selectedItems():
            item.setSelected(False)
        if self.button_pen.isChecked():
            logger.debug("Toggling the comment mode.")
            self.button_pen.setToolTip("Click to enable writing.")
        else:
            logger.debug("Toggling the writing mode.")
            self.button_pen.setToolTip("Click to enable comment.")
        self.table_sudoku.setItemDelegate(DelegateSudokuTable(self.button_pen, self.colors))

    def buttonHintClicked(self) -> None:
        state: QTableWidget = None
        for item in self.table_sudoku.selectedItems():
            state = item
        if not state:
            return

    def buttonNumberClicked(self, button: QPushButton) -> None:
        for item in self.table_sudoku.selectedItems():
            if self.button_pen.isChecked():
                if button.text() in item.text():
                    item.setText(item.text().replace(button.text(), ""))
                else:
                    item.setText("".join(sorted(item.text() + button.text())))
            else:
                item.setText(button.text())
                self.grid[item.row()][item.column()] = int(item.text())
                self.number_is_good()

    def number_is_good(self) -> None:
        for item in self.table_sudoku.selectedItems():
            if not self.button_pen.isChecked():
                if self.grid_solved[item.row()][item.column()] == self.grid[item.row()][item.column()]:
                    item.setForeground(self.colors["item-made"])
                    item.setFlags(Qt.ItemIsEnabled)
                else:
                    item.setForeground(self.colors["item-false"])
                    if self.errors == 3:
                        sys.exit()
                    self.label_errors[self.errors].setFixedSize(50, 50)
                    self.label_errors[self.errors].setAlignment(Qt.AlignCenter)
                    self.label_errors[self.errors].setPixmap(QPixmap(getAbsolutePath("assets", "broken_heart.png")).scaled(32, 32))
                    self.errors += 1
