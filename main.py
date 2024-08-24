import sys
import qdarktheme
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from src.window import Window

def main() -> None:
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    window = Window()
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
