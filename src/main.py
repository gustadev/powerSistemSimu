import sys
import os
import qdarktheme
from typing import *
from PySide6.QtWidgets import QApplication

from view.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    
    if os.name == 'nt' :
        window.setStyleSheet(qdarktheme.load_stylesheet())
    window.resize(640, 480)
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    main()
