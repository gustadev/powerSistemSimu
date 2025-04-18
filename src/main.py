import sys
import os

from typing import *
from PySide6.QtWidgets import QApplication

from components.main_window import MainWindow
from models.circuit_node import BusNode, GeneratorNode, LoadNode
from models.simulator_state import SimulatorState


def main():
    app = QApplication(sys.argv)

    simulatorState = SimulatorState()

    window = MainWindow(
        onRunPowerFlowTap=simulatorState.runPowerFlow,
        onElementLinked=simulatorState.connect,
        onAddBusTap=lambda: simulatorState.setNode(BusNode(v_nom=20.0)),
        onAddLoadTap=lambda: simulatorState.setNode(LoadNode(p_set=100)),
        onAddGeneratorTap=lambda: simulatorState.setNode(
            GeneratorNode(p_set=100, control="PQ")
        ),
    )

    window.resize(640, 480)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    main()
