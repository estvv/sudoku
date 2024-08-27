import sys
import qdarkstyle
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import *
from src.window import Window

def main() -> None:
    global app
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(palette=qdarkstyle.DarkPalette))
    window = Window()
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
