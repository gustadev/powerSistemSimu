from typing import *
from PySide6.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsSimpleTextItem,
)
from PySide6.QtCore import Qt

from controllers.simulator_controller import ElementEvent, SimulatorController
from models.circuit_element import CircuitElement
from view.draggable_link_square import DraggableLinkSquare


class CircuitNodeWidget(QGraphicsRectItem):
    def __init__(self, x: float, y: float, element: CircuitElement):
        super().__init__(x, y, 50, 50)
        self.node = element
        self.setBrush(Qt.gray)
        self.setFlag(QGraphicsRectItem.ItemIsMovable, True)
        self.setFlag(QGraphicsRectItem.ItemIsSelectable, True)

        self.link = DraggableLinkSquare(x + 50 / 2, y + 50 / 2, self)

        self.label = QGraphicsSimpleTextItem(element.name, parent=self)
        self.label.setPos(x + 5, y)
        SimulatorController.instance().listen(self.circuitListener)

    def circuitListener(self, node: CircuitElement, event: ElementEvent):
        if event == ElementEvent.UPDATED and node.id == self.node.id:
            self.node = node
            self.label.setText(node.name)
