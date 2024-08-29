from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MenuSettings(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()

    def initUI(self) -> None:

        self.line_sounds = QLineEdit("50")
        self.line_sounds.setAlignment(Qt.AlignCenter)
        self.scroll_sounds = QScrollBar(self)
        self.scroll_sounds.setFixedSize(300, 50)
        self.scroll_sounds.setOrientation(Qt.Horizontal)
        self.scroll_sounds.setValue(50)
        self.scroll_sounds.valueChanged.connect(self.onSoundChanged)

        self.line_music = QLineEdit("50")
        self.line_music.setAlignment(Qt.AlignCenter)
        self.scroll_music = QScrollBar(self)
        self.scroll_music.setFixedSize(300, 50)
        self.scroll_music.setOrientation(Qt.Horizontal)
        self.scroll_music.setValue(50)
        self.scroll_music.valueChanged.connect(self.onMusicChanged)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.line_sounds)
        layout.setAlignment(self.line_sounds, Qt.AlignCenter)
        layout.addWidget(self.scroll_sounds)
        layout.setAlignment(self.scroll_sounds, Qt.AlignCenter)
        layout.addSpacing(50)
        layout.addWidget(self.line_music)
        layout.setAlignment(self.line_music, Qt.AlignCenter)
        layout.addWidget(self.scroll_music)
        layout.setAlignment(self.scroll_music, Qt.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)

    def onSoundChanged(self):
        self.line_sounds.setText(str(self.scroll_sounds.value()))

    def onMusicChanged(self):
        self.line_music.setText(str(self.scroll_music.value()))
