from typing import *
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout
)

from controllers.simulator_controller import SimulatorController
from view.board_view import BoardView
from view.element_list import ElementList


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        centralWidget = QWidget()
        layout = QVBoxLayout(centralWidget)

        addBusButton = QPushButton("Add Bus")
        addGeneratorButton = QPushButton("Add Generator")
        addLoadButton = QPushButton("Add Load")
        runPowerFlowButton = QPushButton("Run Power Flow")
        printNetworkButton = QPushButton("Print Network")

        # Create the board view.
        board = BoardView()
        simulatorInstance = SimulatorController.instance()

        # Connect button signal to the board's addSquare method.
        addBusButton.clicked.connect(simulatorInstance.addBus)
        addLoadButton.clicked.connect(simulatorInstance.addLoad)
        addGeneratorButton.clicked.connect(simulatorInstance.addGenerator)
        runPowerFlowButton.clicked.connect(simulatorInstance.runPowerFlow)
        printNetworkButton.clicked.connect(simulatorInstance.printNetwork)

        # Add widgets to the layout.
        layout.addWidget(addBusButton)
        layout.addWidget(addGeneratorButton)
        layout.addWidget(addLoadButton)
        layout.addWidget(board)

        # Create a horizontal layout to place the board view on the left and a new widget on the right.
        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(board)
        
        rightWidget = ElementList()
        rightWidget.setMaximumWidth(200)  
        rightWidget.setMinimumWidth(200)
        horizontalLayout.addWidget(rightWidget)
        
        layout.addLayout(horizontalLayout)
        layout.addWidget(runPowerFlowButton)
        layout.addWidget(printNetworkButton)

        self.setCentralWidget(centralWidget)
