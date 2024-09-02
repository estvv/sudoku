from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src import *

class SettingsGUI(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initGUI()

    def initGUI(self) -> None:
        self.initSound()
        self.initMusic()

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.label_sounds_icon)
        layout.setAlignment(self.label_sounds_icon, Qt.AlignCenter)
        layout.addWidget(self.line_sounds)
        layout.setAlignment(self.line_sounds, Qt.AlignCenter)
        layout.addWidget(self.scroll_sounds)
        layout.setAlignment(self.scroll_sounds, Qt.AlignCenter)
        layout.addSpacing(50)
        layout.addWidget(self.label_music_icon)
        layout.setAlignment(self.label_music_icon, Qt.AlignCenter)
        layout.addWidget(self.line_music)
        layout.setAlignment(self.line_music, Qt.AlignCenter)
        layout.addWidget(self.scroll_music)
        layout.setAlignment(self.scroll_music, Qt.AlignCenter)
        layout.addStretch()

        frame = QFrame()
        frame.setFrameShape(QFrame.Box)
        frame.setLineWidth(2)
        frame.setFixedSize(400, 400)
        frame.setLayout(layout)

        main_layout = QVBoxLayout()
        main_layout.addStretch()
        main_layout.addWidget(frame)
        main_layout.setAlignment(frame, Qt.AlignCenter)
        main_layout.addStretch()
        self.setLayout(main_layout)

    def initSound(self):
        self.label_sounds_icon = QLabel()
        self.label_sounds_icon.setFixedSize(50, 50)
        self.label_sounds_icon.setAlignment(Qt.AlignCenter)
        self.label_sounds_icon.setPixmap(QPixmap(getAbsolutePath("assets", "sound_2.png")).scaled(32, 32))

        self.line_sounds = QLineEdit("50")
        self.line_sounds.setValidator(QIntValidator(0, 100, self))
        self.line_sounds.setAlignment(Qt.AlignCenter)
        self.line_sounds.textChanged.connect(self.onSoundNumberChanged)
        self.scroll_sounds = QScrollBar(self)
        self.scroll_sounds.setMaximum(100)
        self.scroll_sounds.setFixedSize(300, 50)
        self.scroll_sounds.setValue(50)
        self.scroll_sounds.setOrientation(Qt.Horizontal)
        self.scroll_sounds.valueChanged.connect(self.onSoundChanged)

    def initMusic(self):
        self.label_music_icon = QLabel()
        self.label_music_icon.setFixedSize(50, 50)
        self.label_music_icon.setAlignment(Qt.AlignCenter)
        self.label_music_icon.setPixmap(QPixmap(getAbsolutePath("assets", "music.png")).scaled(32, 32))

        self.line_music = QLineEdit("50")
        self.line_music.setValidator(QIntValidator(0, 100, self))
        self.line_music.setAlignment(Qt.AlignCenter)
        self.line_music.textChanged.connect(self.onMusicNumberChanged)
        self.scroll_music = QScrollBar(self)
        self.scroll_music.setMaximum(100)
        self.scroll_music.setFixedSize(300, 50)
        self.scroll_music.setValue(50)
        self.scroll_music.setOrientation(Qt.Horizontal)
        self.scroll_music.valueChanged.connect(self.onMusicChanged)

    def onSoundChanged(self):
        self.line_sounds.setText(str(self.scroll_sounds.value()))
        if self.scroll_sounds.value() == 0:
            self.label_sounds_icon.setPixmap(QPixmap(getAbsolutePath("assets", "sound_0.png")).scaled(32, 32))
        elif self.scroll_sounds.value() <= 30:
            self.label_sounds_icon.setPixmap(QPixmap(getAbsolutePath("assets", "sound_1.png")).scaled(32, 32))
        elif self.scroll_sounds.value() <= 70:
            self.label_sounds_icon.setPixmap(QPixmap(getAbsolutePath("assets", "sound_2.png")).scaled(32, 32))
        else:
            self.label_sounds_icon.setPixmap(QPixmap(getAbsolutePath("assets", "sound_3.png")).scaled(32, 32))

    def onSoundNumberChanged(self):
        if len(self.line_sounds.text()) > 0:
            self.scroll_sounds.setValue(int(self.line_sounds.text()))

    def onMusicChanged(self):
        self.line_music.setText(str(self.scroll_music.value()))

    def onMusicNumberChanged(self):
        if len(self.line_music.text()) > 0:
            self.scroll_music.setValue(int(self.line_music.text()))
