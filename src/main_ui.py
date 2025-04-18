import string
import sys
from typing import *
import PySide6
import numpy as np
import pypsa
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsRectItem,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QGraphicsLineItem,
    QGraphicsSimpleTextItem,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtGui import QPen
import os

network = pypsa.Network()


class LinkLineItem(QGraphicsLineItem):
    def __init__(self, widget1, widget2):
        super().__init__()
        self.widget1 = widget1
        self.widget2 = widget2
        self.setPen(QPen(Qt.black, 2))
        self.setZValue(0)  # So that it stays behind the squares

    def updatePosition(self):
        p1 = self.widget1.sceneBoundingRect().center()
        p2 = self.widget2.sceneBoundingRect().center()
        self.setLine(p1.x(), p1.y(), p2.x(), p2.y())

    def paint(self, painter, option, widget):
        self.updatePosition()
        super().paint(painter, option, widget)


class BoardView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        self.setSceneRect(0, 0, 600, 400)
        self.elementCount = dict()
        self.elements = dict()
        self.lastFocused = None

    def addElementToCollections(self, class_name: string):
        if class_name not in self.elementCount:
            self.elementCount[class_name] = 0
        self.elementCount[class_name] += 1
        element = f"{class_name} {self.elementCount[class_name]}"

        if class_name not in self.elements:
            self.elements[class_name] = []
        self.elements[class_name].append(element)

        return (element, self.elementCount[class_name])

    def addVisualAndElectricElement(self, class_name: string, **kwargs: Any):
        # Update collections
        (element, count) = self.addElementToCollections(class_name)

        # Add the element to the network
        network.add(class_name, element, **kwargs)

        # Add the visual representation
        x = 50 + count * 70
        y = 50
        square = QGraphicsRectItem(x, y, 50, 50)
        square.setBrush(Qt.gray)
        square.setFlag(QGraphicsRectItem.ItemIsMovable, True)
        square.setFlag(QGraphicsRectItem.ItemIsSelectable, True)
        self.scene().addItem(square)

        # Add link button
        red_square = QGraphicsRectItem(x + 50 / 2, y + 50 / 2, 10, 10, parent=square)
        red_square.setBrush(Qt.red)
        red_square.setFlag(QGraphicsRectItem.ItemIsSelectable, True)
        red_square.setFlag(QGraphicsRectItem.ItemIsFocusable, True)
        red_square.focusInEvent = lambda event: self.onLinkFocused(red_square, element)

        # Add label
        label = QGraphicsSimpleTextItem(element, parent=square)
        label.setPos(x + 5, y)

    def onLinkFocused(self, widget: QGraphicsRectItem, element: string):
        if self.lastFocused == None:
            self.lastFocused = (widget, element)
            print("Selected link:", widget)
            return
        
        if(not element.startswith("Bus") and not self.lastFocused[1].startswith("Bus")):
            print("Cannot link non-bus elements")
            self.lastFocused = None
            return
        
        if element.startswith("Bus") and self.lastFocused[1].startswith("Bus"):
            (line, count) = self.addElementToCollections("Line")

            network.add(
                "Line", line, bus0=element, bus1=self.lastFocused[1], x=0.1, r=0.01
            )

            print("Added line:", line)
            self.scene().addItem(LinkLineItem(widget, self.lastFocused[0]))
            self.lastFocused = None
            return

        if element.startswith("Bus") and self.lastFocused[1].startswith("Generator"):
            network.add(
                "Generator",
                self.lastFocused[1],
                bus=element,
                p_set=100,
                control="PQ",
                overwrite=True,
            )
            self.scene().addItem(LinkLineItem(widget, self.lastFocused[0]))
            self.lastFocused = None
            return

        if element.startswith("Bus") and self.lastFocused[1].startswith("Load"):
            network.add(
                "Load", self.lastFocused[1], bus=element, p_set=100, overwrite=True
            )
            print("Linked load:", self.lastFocused[1])
            self.scene().addItem(LinkLineItem(widget, self.lastFocused[0]))
            self.lastFocused = None
            return

        self.lastFocused = None

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
            for item in self.scene().selectedItems():
                self.scene().removeItem(item)
        else:
            super().keyPressEvent(event)

    def runPowerFlow(self):
        network.pf()
        print("Power flow results:")
        print(network.lines_t.p0)
        print(network.buses_t.v_ang * 180 / np.pi)
        print(network.buses_t.v_mag_pu)


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
    # layout.addWidget(addTransformerButton)
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
