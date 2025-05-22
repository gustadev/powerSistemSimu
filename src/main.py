import sys
import os
import qdarktheme
from typing import *
from PySide6.QtWidgets import QApplication

from controllers.simulator_controller import SimulatorController
from models.bus import Bus, BusType
from models.line import Line
from view.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    window = MainWindow()

    if os.name == "nt":
        window.setStyleSheet(qdarktheme.load_stylesheet())  # 'light'
    window.resize(640, 480)
    window.show()

    # instance: SimulatorController = SimulatorController.instance()
    # bus1 = instance.addBus(Bus(name="Slack Bus", v=1.05, type=BusType.SLACK))
    # bus2 = instance.addBus(Bus(name="Load", p_load=4, q_load=2.5, type=BusType.PQ))
    # bus3 = instance.addBus(Bus(name="Generator", v=1.04, p_gen=2, type=BusType.PV))

    # instance.addConnection(Line.from_z(bus1, bus2, z=complex(0.02, 0.04)))
    # instance.addConnection(Line.from_z(bus2, bus3, z=complex(0.0125, 0.025)))
    # instance.addConnection(Line.from_z(bus3, bus1, z=complex(0.01, 0.03)))

    sys.exit(app.exec())


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    main()
