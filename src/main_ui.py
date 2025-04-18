import sys
from typing import *
import pypsa
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
)
import os

from components.board_view import BoardView

network = pypsa.Network()

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()

    # Create a central widget and layout.
    centralWidget = QWidget()
    layout = QVBoxLayout(centralWidget)

    # Create the button to add squares.
    addBusButton = QPushButton("Add Bus")
    # addTransformerButton = QPushButton("Add Transformer")
    addGeneratorButton = QPushButton("Add Generator")
    addLoadButton = QPushButton("Add Load")

    runPowerFlowButton = QPushButton("Run Power Flow")

    # Create the board view.
    board = BoardView(network=network)

    # Connect button signal to the board's addSquare method.
    addBusButton.clicked.connect(
        lambda: board.addVisualAndElectricElement("Bus", v_nom=20.0)
    )
    addLoadButton.clicked.connect(
        lambda: board.addVisualAndElectricElement("Load", p_set=100)
    )
    addGeneratorButton.clicked.connect(
        lambda: board.addVisualAndElectricElement("Generator", p_set=100, control="PQ")
    )
    runPowerFlowButton.clicked.connect(lambda: board.runPowerFlow())

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
