import sys
import os
import qdarktheme
from typing import *
from PySide6.QtWidgets import QApplication

from controllers.simulator_controller import SimulatorController
from view.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    window = MainWindow()

    if os.name == "nt":
        window.setStyleSheet(qdarktheme.load_stylesheet())  # 'light'
    window.resize(640, 480)
    window.show()

    instance: SimulatorController = SimulatorController.instance()
    b1 = instance.addBus()
    b2 = instance.addBus()
    instance.addConnection(b1, b2)

    sys.exit(app.exec())


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    main()
