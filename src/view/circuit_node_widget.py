from typing import *
from PySide6.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsSimpleTextItem,
)
from PySide6.QtCore import Qt

from controllers.simulator_controller import ElementEvent, SimulatorController
from models.bus import Bus
from models.network_element import NetworkElement
from view.draggable_link_square import DraggableLinkSquare


class CircuitNodeWidget(QGraphicsRectItem):
    def __init__(self, x: float, y: float, bus: Bus):
        super().__init__(x, y, 50, 50)
        self.bus = bus
        self.setBrush(Qt.GlobalColor.gray)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable, True)

        self.link = DraggableLinkSquare(x + 50 / 2, y + 50 / 2, self)

        self.label = QGraphicsSimpleTextItem(bus.name, parent=self)
        self.label.setPos(x + 5, y)
        SimulatorController.instance().listen(self.circuitListener)

    def circuitListener(self, node: NetworkElement, event: ElementEvent):
        if event == ElementEvent.UPDATED and node.id == self.bus.id:
            self.bus = node
            self.label.setText(node.name)
