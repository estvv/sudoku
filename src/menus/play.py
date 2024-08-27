import qdarkstyle
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.logger import *
from src.tools import *
from src.enums.enums import *
from src.buttons.slicing_button import *

class TableDelegate(QStyledItemDelegate):
    def __init__(self, button_pen, parent = None) -> None:
        super().__init__(parent)
        self.button_pen = button_pen
        self.previous_text = ""
        self.recursion_error = False

    def paint(self, painter, option, index) -> None:
        super().paint(painter, option, index)

        if (index.column() + 1) % 3 == 0 and (index.column() + 1) != 9:
            pen = QPen(Qt.gray, 2)
            painter.setPen(pen)
            painter.drawLine(option.rect.topRight(), option.rect.bottomRight())
        if (index.row() + 1) % 3 == 0 and (index.row() + 1) != 9:
            pen = QPen(Qt.gray, 2)
            painter.setPen(pen)
            painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())

    def createEditor(self, parent, option, index) -> None:
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

    def onTextChanged(self, text) -> None:
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

    def setEditorData(self, editor, index) -> None:
        text = index.data(Qt.DisplayRole)
        if text is None:
            text = ""
        editor.setText(text)
        self.previous_text = text

class MenuPlay(QWidget):
    font: QFont = None
    theme: ThemeID = ThemeID.dark

    def __init__(self) -> None:
        super().__init__()
        self.font = QFont("Arial", 12)
        self.initUI()

    def initUI(self):
        self.button_theme = SlicingButton("", QColor(255, 255, 255), QColor(0, 0, 0), self)
        self.button_theme.animation.finished.connect(self.buttonThemeAnimationFinished)
        layout_top = QHBoxLayout()
        layout_top.addStretch()
        layout_top.addWidget(self.button_theme)
        layout_top.addStretch()

        layout_tools = self.initTools()
        self.initSudokuTable()
        layout_numbers = self.initNumbers()

        layout_play = QVBoxLayout()
        layout_play.addLayout(layout_top)
        layout_play.addWidget(self.table_sudoku)
        layout_play.setAlignment(self.table_sudoku, Qt.AlignHCenter)
        layout_play.addLayout(layout_tools)
        layout_play.setAlignment(layout_tools, Qt.AlignHCenter)
        layout_play.addLayout(layout_numbers)
        layout_play.setAlignment(layout_numbers, Qt.AlignHCenter)
        self.setLayout(layout_play)

    def initTools(self) -> QHBoxLayout:
        layout_tools = QHBoxLayout()
        self.button_erase = getButton(self.buttonEraseClicked, "", [100, 50])
        self.button_erase.setIcon(QIcon(getAbsolutePath("assets", "eraser.png")))
        self.button_erase.setIconSize(QSize(32, 32))
        self.button_erase.setToolTip("Click to erase a box.")

        self.button_pen = getButton(self.buttonPenClicked, "", [100, 50])
        self.button_pen.setIcon(QIcon(getAbsolutePath("assets", "pen.png")))
        self.button_pen.setIconSize(QSize(32, 32))
        self.button_pen.setCheckable(True)
        self.button_pen.setToolTip("Click to enable comment.")

        self.tableDelegate = TableDelegate(self.button_pen)

        self.button_hint = getButton(lambda: None, "  0 / 3", [100, 50])
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
        self.table_sudoku.setItemDelegate(self.tableDelegate)
        self.table_sudoku.horizontalHeader().setVisible(False)
        self.table_sudoku.verticalHeader().setVisible(False)
        self.table_sudoku.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_sudoku.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_sudoku.setSelectionMode(QAbstractItemView.SingleSelection)

        for i in range(9):
            for j in range(9):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(self.font)
                self.table_sudoku.setItem(i, j, item)
        self.updateTheme(QColor("white"), QColor("black"), QColor("#1e1e1e"))
        self.table_sudoku.itemClicked.connect(self.some_function)

    def some_function(self):
        for item in self.table_sudoku.selectedItems():
            if self.button_pen.isChecked():
                item.setForeground(QColor(128, 128, 128))
            else:
                if self.theme == ThemeID.dark:
                    item.setForeground(QColor("white"))
                else:
                    item.setForeground(QColor("black"))

    def initNumbers(self) -> QHBoxLayout:
        layout_numbers = QHBoxLayout()
        self.buttonsNumber: list[QPushButton] = []
        for i in range(1, 10):
            self.buttonsNumber.append(getSelfButton(self.buttonNumberClicked, str(i), [95, 50]))
        for i in range(len(self.buttonsNumber)):
            layout_numbers.addWidget(self.buttonsNumber[i])
        return layout_numbers

    def buttonThemeAnimationFinished(self):
        app = QApplication.instance()

        if self.button_theme.slider_pos > 0:
            app.setStyleSheet(qdarkstyle.load_stylesheet(palette=qdarkstyle.LightPalette))
            logger.info("Light")
            self.button_theme.setText("")
            self.updateTheme( QColor("black"), QColor("white"), QColor("#f0f0f0"))
            self.theme = ThemeID.light
        else:
            app.setStyleSheet(qdarkstyle.load_stylesheet(palette=qdarkstyle.DarkPalette))
            logger.info("Dark")
            self.button_theme.setText("")
            self.updateTheme( QColor("white"), QColor("black"), QColor("#1e1e1e"))
            self.theme = ThemeID.dark

    def updateTheme(self, foreground_color: QColor, background_color: QColor, selected_background_color: QColor):
        for i in range(9):
            for j in range(9):
                item = self.table_sudoku.item(i, j)
                item.setBackground(background_color)
                if item.foreground().color() == QColor("white") or item.foreground().color() == QColor("black"):
                    item.setForeground(foreground_color)

        self.table_sudoku.setStyleSheet(f"""
            QTableWidget::item:selected {{
                background-color: {selected_background_color.name()};
                border: 1px solid {selected_background_color.darker().name()};
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
        self.tableDelegate = TableDelegate(self.button_pen)
        self.table_sudoku.setItemDelegate(self.tableDelegate)

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
