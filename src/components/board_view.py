
import string
from typing import *
import numpy as np
from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QGraphicsRectItem,
    QGraphicsSimpleTextItem,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter

from components.draggable_link_square import DraggableLinkSquare
from components.link_line_item import LinkLineItem

class BoardView(QGraphicsView):
    def __init__(self, network):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        self.setSceneRect(0, 0, 600, 400)
        self.elementCount = dict()
        self.elements = dict()
        self.network = network

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
        self.network.add(class_name, element, **kwargs)

        # Add the visual representation
        x = 50 + count * 70
        y = 50
        square = QGraphicsRectItem(x, y, 50, 50)
        square.setBrush(Qt.gray)
        square.setFlag(QGraphicsRectItem.ItemIsMovable, True)
        square.setFlag(QGraphicsRectItem.ItemIsSelectable, True)
        self.scene().addItem(square)

        DraggableLinkSquare(x + 50 / 2, y + 50 / 2, element, square, self)

        # Add label
        label = QGraphicsSimpleTextItem(element, parent=square)
        label.setPos(x + 5, y)

    def onLinkConnected(self, source: DraggableLinkSquare, target: DraggableLinkSquare):
        if not source.element.startswith("Bus") and not target.element.startswith(
            "Bus"
        ):
            print("Cannot link non-bus elements")
            self.lastFocused = None
            return

        if source.element.startswith("Bus") and target.element.startswith("Bus"):
            (line, count) = self.addElementToCollections("Line")

            self.network.add(
                "Line", line, bus0=source.element, bus1=target.element, x=0.1, r=0.01
            )

            self.scene().addItem(LinkLineItem(source, target))
            self.lastFocused = None
            return

        if source.element.startswith("Bus") and target.element.startswith("Generator"):
            self.network.add(
                "Generator",
                target.element,
                bus=source.element,
                p_set=100,
                control="PQ",
                overwrite=True,
            )
            self.scene().addItem(LinkLineItem(source, target))
            self.lastFocused = None
            return

        if source.element.startswith("Bus") and target.element.startswith("Load"):
            self.network.add(
                "Load", target.element, bus=source.element, p_set=100, overwrite=True
            )
            print("Linked load:", target.element)
            self.scene().addItem(LinkLineItem(source, target))
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
        self.network.pf()
        print("Power flow results:")
        print(self.network.lines_t.p0)
        print(self.network.buses_t.v_ang * 180 / np.pi)
        print(self.network.buses_t.v_mag_pu)
