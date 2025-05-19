from typing import *
from PySide6.QtWidgets import (
    QGraphicsLineItem,
)
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsSimpleTextItem
from PySide6.QtGui import QPen

from controllers.simulator_controller import ElementEvent, SimulatorController
from models.connection import BusConnection
from models.network_element import NetworkElement


class LinkLineItem(QGraphicsLineItem):
    def __init__(
        self,
        sourceNodeDraggableLink,
        targetNodeDraggableLink,
        connection: BusConnection,
    ):
        super().__init__()
        self.sourceNodeDraggableLink = sourceNodeDraggableLink
        self.targetNodeDraggableLink = targetNodeDraggableLink
        self.setPen(QPen(Qt.blue, 1))
        self.setZValue(0)
        self.connection: BusConnection = connection
        self.nameLabel = None
        self.center = None
        if isinstance(connection, BusConnection):
            self.nameLabel = QGraphicsSimpleTextItem(connection.name)
            self.nameLabel.setBrush(Qt.white)
            self.nameLabel.setParentItem(self)
            SimulatorController.instance().listen(self.circuitListener)

    def updatePosition(self):
        p1 = self.sourceNodeDraggableLink.sceneBoundingRect().center()
        p2 = self.targetNodeDraggableLink.sceneBoundingRect().center()
        self.setLine(p1.x(), p1.y(), p2.x(), p2.y())
        if self.nameLabel:
            self.center = p1 + (p2 - p1) / 2
            self.nameLabel.setPos(self.center.x(), self.center.y())

    def paint(self, painter, option, widget):
        self.updatePosition()
        super().paint(painter, option, widget)

    def circuitListener(self, element: NetworkElement, event: ElementEvent):
        if event == ElementEvent.UPDATED and self.connection.id == element.id:
            self.connection = element
            self.nameLabel.setText(element.name)
