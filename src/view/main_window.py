from typing import *
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout

from controllers.simulator_controller import SimulatorController
from view.board_view import BoardView
from view.element_list import ElementList


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        centralWidget = QWidget()
        self.setWindowTitle("Power Systems Simulator")
        # Layout creation
        layoutBtnElements = QHBoxLayout()
        layoutBtnActions = QHBoxLayout()
        horizontalLayout = QHBoxLayout()

        # Layout Alignment configuration
        layoutBtnElements.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layoutBtnActions.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Screen montage
        layout = QVBoxLayout(centralWidget)
        layout.addLayout(layoutBtnElements)
        layout.addLayout(horizontalLayout)
        layout.addLayout(layoutBtnActions)

        addBusButton = QPushButton("")  # ("Add Bus")
        addBusButton.setFixedSize(60, 35)
        addBusButton.setIcon(QIcon("assets/ico/busbar.png"))
        addBusButton.setIconSize(QSize(70, 30))

        addGeneratorButton = QPushButton("")  # ("Add Generator")
        addGeneratorButton.setFixedSize(60, 35)
        addGeneratorButton.setIcon(QIcon("assets/ico/gerador.png"))
        addGeneratorButton.setIconSize(QSize(70, 30))

        addLoadButton = QPushButton("")  # ("Add Load")
        addLoadButton.setFixedSize(60, 35)
        addLoadButton.setIconSize(QSize(70, 30))
        addLoadButton.setIcon(QIcon("assets/ico/load.png"))

        runPowerFlowButton = QPushButton("Run Power Flow")
        runPowerFlowButton.setFixedSize(110, 30)

        printNetworkButton = QPushButton("Print Network")
        printNetworkButton.setFixedSize(110, 30)

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
        layoutBtnElements.addWidget(addBusButton)
        layoutBtnElements.addWidget(addGeneratorButton)
        layoutBtnElements.addWidget(addLoadButton)
        layoutBtnElements.addWidget(board)

        # Create a horizontal layout to place the board view on the left and a new widget on the right.

        rightWidget = ElementList()
        rightWidget.setMaximumWidth(200)
        rightWidget.setMinimumWidth(200)
        horizontalLayout.addWidget(board)
        horizontalLayout.addWidget(rightWidget)
        # horizontalLayout.setContentsMargins(5, 5, 5, 5)

        layoutBtnActions.addWidget(runPowerFlowButton)
        layoutBtnActions.addWidget(printNetworkButton)

        self.setCentralWidget(centralWidget)
