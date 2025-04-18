import sys
from typing import *
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
)
import os

from components.board_view import BoardView
from models.circuit_node import BusNode, CircuitNode, GeneratorNode, LoadNode
from models.simulator_state import SimulatorState


def main():
    app = QApplication(sys.argv)
    simulatorState = SimulatorState()
    window = QMainWindow()

    # Create a central widget and layout.
    centralWidget = QWidget()
    layout = QVBoxLayout(centralWidget)

    # Create the button to add squares.
    addBusButton = QPushButton("Add Bus")
    addGeneratorButton = QPushButton("Add Generator")
    addLoadButton = QPushButton("Add Load")
    runPowerFlowButton = QPushButton("Run Power Flow")

    # Create the board view.
    board = BoardView()
    board.onElementLinked = simulatorState.connect

    def addNode(newNode: CircuitNode):
        simulatorState.setNode(newNode)
        board.addNodeWidget(newNode.name)

    # Connect button signal to the board's addSquare method.
    addBusButton.clicked.connect(lambda: addNode(BusNode(v_nom=20.0)))
    addLoadButton.clicked.connect(lambda: addNode(LoadNode(p_set=100)))
    addGeneratorButton.clicked.connect(
        lambda: addNode(GeneratorNode(p_set=100, control="PQ"))
    )
    runPowerFlowButton.clicked.connect(lambda: simulatorState.runPowerFlow())

    # Add widgets to the layout.
    layout.addWidget(addBusButton)
    layout.addWidget(addGeneratorButton)
    layout.addWidget(addLoadButton)
    layout.addWidget(board)
    layout.addWidget(runPowerFlowButton)

    window.setCentralWidget(centralWidget)
    window.resize(640, 480)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    main()
