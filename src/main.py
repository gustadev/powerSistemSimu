import sys
import os

from typing import *
from PySide6.QtWidgets import QApplication

from view.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    window = MainWindow()

    window.resize(640, 480)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    main()
