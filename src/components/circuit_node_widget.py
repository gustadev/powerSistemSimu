from typing import *
from PySide6.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsSimpleTextItem,
)
from PySide6.QtCore import Qt

from components.draggable_link_square import DraggableLinkSquare
from models.circuit_node import CircuitNode


class CircuitNodeWidget(QGraphicsRectItem):
    def __init__(self, x:float,y:float, node: CircuitNode):
        super().__init__(x, y, 50, 50)
        self.node = node
        self.setBrush(Qt.gray)
        self.setFlag(QGraphicsRectItem.ItemIsMovable, True)
        self.setFlag(QGraphicsRectItem.ItemIsSelectable, True)

        self.link = DraggableLinkSquare(x + 50 / 2, y + 50 / 2, self)

        label = QGraphicsSimpleTextItem(node.name, parent=self)
        label.setPos(x + 5, y)
