from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtProperty

class SlicingButton(QPushButton):
    slider_pos: int = 0
    target_pos: int = 0
    color_on: QColor = None
    color_off: QColor = None

    def __init__(self, text: str, w: int, h: int, color_on: QColor, color_off: QColor, parent = None) -> None:
        super().__init__(text, parent)
        self.setFixedSize(w, h)
        self.color_on = color_on
        self.color_off = color_off
        self.slider_pos = 0
        self.target_pos = self.width()
        self.animation = QPropertyAnimation(self, b"slice_position")
        self.animation.setDuration(500)

    @pyqtProperty(int)
    def slice_position(self) -> int:
        return self.slider_pos

    @slice_position.setter
    def slice_position(self, value: int) -> None:
        self.slider_pos = value
        self.update()

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.animation.setStartValue(self.slider_pos)
            if self.slider_pos == 0:
                self.animation.setEndValue(self.target_pos)
            else:
                self.animation.setEndValue(0)
            self.animation.start()
        super().mousePressEvent(event)

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        painter = QPainter(self)
        rect = self.rect()

        if self.slider_pos > 0:
            painter.setBrush(QBrush(self.color_on))
            painter.drawRect(QRectF(rect.left(), rect.top(), self.slider_pos, rect.height()).adjusted(0, 0, -1, -1))

            painter.setBrush(QBrush(self.color_off))
            painter.drawRect(QRectF(self.slider_pos, rect.top(), rect.width() - self.slider_pos, rect.height()).adjusted(0, 0, -1, -1))
            painter.setPen(self.color_off)
            painter.drawText(rect, Qt.AlignCenter, self.text())
        else:
            painter.setBrush(QBrush(self.color_off))
            painter.drawRect(QRectF(rect.left(), rect.top(), rect.width(), rect.height()).adjusted(0, 0, -1, -1))
            painter.setPen(self.color_on)
            painter.drawText(rect, Qt.AlignCenter, self.text())
