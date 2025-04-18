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
        self.onElementLinked: Callable = None

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

        DraggableLinkSquare(
            x + 50 / 2,
            y + 50 / 2,
            element,
            square,
            onConnectionStart=self.onLinkConnected,
        )

        # Add label
        label = QGraphicsSimpleTextItem(element, parent=square)
        label.setPos(x + 5, y)

    def onLinkConnected(self, source: DraggableLinkSquare, target: DraggableLinkSquare):
        canLink = self.onElementLinked(source.element, target.element)
        if canLink:
            self.scene().addItem(LinkLineItem(source, target))

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
            for item in self.scene().selectedItems():
                self.scene().removeItem(item)
        else:
            super().keyPressEvent(event)
