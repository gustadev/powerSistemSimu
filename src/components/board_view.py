import string
from typing import *
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
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        self.setSceneRect(0, 0, 600, 400)
        self.onElementLinked: Callable = None

    def addVisualAndElectricElement(self, element: string, count: int):
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
        (canLink,name) = self.onElementLinked(source.element, target.element)
        if canLink:
            self.scene().addItem(LinkLineItem(source, target, name))

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
            for item in self.scene().selectedItems():
                self.scene().removeItem(item)
        else:
            super().keyPressEvent(event)
