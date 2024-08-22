import sys
from src.window import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import qdarktheme

def main() -> None:
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    window = Window()
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
