import string
import sys
from typing import *
import numpy as np
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
from components.link_line_item import LinkLineItem
from models.simulator_state import SimulatorState

network = pypsa.Network()
simulatorState = SimulatorState()


def runPowerFlow():
    network.pf()
    print("Power flow results:")
    print(network.lines_t.p0)
    print(network.buses_t.v_ang * 180 / np.pi)
    print(network.buses_t.v_mag_pu)


def onElementLinked(board: BoardView, source: string, target: string):
    if not source.startswith("Bus") and not target.startswith("Bus"):
        print("Cannot link non-bus elements")
        return (False,None)

    if source.startswith("Bus") and target.startswith("Bus"):
        (line, _) = simulatorState.addElement("Line")
        network.add("Line", line, bus0=source, bus1=target, x=0.1, r=0.01)
        print(f"{line} added between {source} and {target}")
        return (True,line)

    if source.startswith("Bus") and target.startswith("Generator"):
        network.add(
            "Generator",
            target,
            bus=source,
            p_set=100,
            control="PQ",
            overwrite=True,
        )
        print(f"{target} added to {source}")
        return (True,None)
    
    if source.startswith("Generator") and target.startswith("Bus"):
        network.add(
            "Generator",
            source,
            bus=target,
            p_set=100,
            control="PQ",
            overwrite=True,
        )
        print(f"{source} added to {target}")
        return (True,None)
    

    if source.startswith("Bus") and target.startswith("Load"):
        network.add("Load", target, bus=source, p_set=100, overwrite=True)
        print(f"{target} added to {source}")
        return (True,None)
    
    if source.startswith("Load") and target.startswith("Bus"):
        network.add("Load", source, bus=target, p_set=100, overwrite=True)
        print(f"{source} added to {target}")
        return (True,None)
    
    return (False,None)


def addNode(board: BoardView, class_name: string, **kwargs):
    (element, count) = simulatorState.addElement(class_name)
    network.add(class_name, element, **kwargs)
    board.addVisualAndElectricElement(element, count)
    print(f"{element} added to the board, with {kwargs}")


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
    board = BoardView()
    board.onElementLinked = lambda source, target: onElementLinked(
        board, source, target
    )

    # Connect button signal to the board's addSquare method.
    addBusButton.clicked.connect(lambda: addNode(board, "Bus", v_nom=20.0))
    addLoadButton.clicked.connect(lambda: addNode(board, "Load", p_set=100))
    addGeneratorButton.clicked.connect(
        lambda: addNode(board, "Generator", p_set=100, control="PQ")
    )
    runPowerFlowButton.clicked.connect(lambda: runPowerFlow())

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
