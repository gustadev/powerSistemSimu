from typing import *
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
)

from components.board_view import BoardView


# TODO make every callcable return string, receibe 2 strings too
class MainWindow(QMainWindow):
    def __init__(
        self,
        onAddBusTap: Callable,
        onAddGeneratorTap: Callable,
        onAddLoadTap: Callable,
        onRunPowerFlowTap: Callable,
        onElementLinked: Callable,
    ):
        super().__init__()
        centralWidget = QWidget()
        layout = QVBoxLayout(centralWidget)

        addBusButton = QPushButton("Add Bus")
        addGeneratorButton = QPushButton("Add Generator")
        addLoadButton = QPushButton("Add Load")
        runPowerFlowButton = QPushButton("Run Power Flow")

        # Create the board view.
        board = BoardView()
        board.onElementLinked = onElementLinked

        def onAddElementWrapper(callable: Callable):
            def createNodeWrapper():
                nodeName = callable()
                if nodeName:
                    board.addNodeWidget(nodeName)

            return createNodeWrapper

        # Connect button signal to the board's addSquare method.
        addBusButton.clicked.connect(onAddElementWrapper(onAddBusTap))
        addLoadButton.clicked.connect(onAddElementWrapper(onAddLoadTap))
        addGeneratorButton.clicked.connect(onAddElementWrapper(onAddGeneratorTap))
        runPowerFlowButton.clicked.connect(onAddElementWrapper(onRunPowerFlowTap))

        # Add widgets to the layout.
        layout.addWidget(addBusButton)
        layout.addWidget(addGeneratorButton)
        layout.addWidget(addLoadButton)
        layout.addWidget(board)
        layout.addWidget(runPowerFlowButton)

        self.setCentralWidget(centralWidget)
