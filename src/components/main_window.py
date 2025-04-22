from typing import *
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
)

from components.board_view import BoardView
from models.simulator_state import SimulatorState


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        centralWidget = QWidget()
        layout = QVBoxLayout(centralWidget)

        addBusButton = QPushButton("Add Bus")
        addGeneratorButton = QPushButton("Add Generator")
        addLoadButton = QPushButton("Add Load")
        runPowerFlowButton = QPushButton("Run Power Flow")

        # Create the board view.
        board = BoardView()
        simulatorInstance = SimulatorState.instance()

        # Connect button signal to the board's addSquare method.
        addBusButton.clicked.connect(simulatorInstance.addBus)
        addLoadButton.clicked.connect(simulatorInstance.addLoad)
        addGeneratorButton.clicked.connect(simulatorInstance.addGenerator)
        runPowerFlowButton.clicked.connect(simulatorInstance.runPowerFlow)

        # Add widgets to the layout.
        layout.addWidget(addBusButton)
        layout.addWidget(addGeneratorButton)
        layout.addWidget(addLoadButton)
        layout.addWidget(board)
        layout.addWidget(runPowerFlowButton)

        self.setCentralWidget(centralWidget)
