from typing import *
from PySide6.QtWidgets import (
    QGraphicsLineItem,
)
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsSimpleTextItem
from PySide6.QtGui import QPen

from controllers.simulator_controller import ElementEvent, SimulatorController
from models.line import Line
from models.network_element import NetworkElement


class LinkLineItem(QGraphicsLineItem):
    def __init__(
        self,
        sourceNodeDraggableLink,
        targetNodeDraggableLink,
        line: Line,
    ):
        super().__init__()
        self.sourceNodeDraggableLink = sourceNodeDraggableLink
        self.targetNodeDraggableLink = targetNodeDraggableLink
        self.setPen(QPen(Qt.blue, 1))
        self.setZValue(0)
        self.__line: Line = line
        self.nameLabel = None
        self.center = None

        self.nameLabel = QGraphicsSimpleTextItem(self.__label)
        self.nameLabel.setBrush(Qt.red)
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
        if (
            event == ElementEvent.UPDATED
            and self.__line.id == element.id
            and isinstance(element, Line)
        ):
            self.__line = element
            self.nameLabel.setText(self.__label)

    @property
    def __label(self) -> str:
        label: str = f"y={self.__line.y:.2f}"
        if self.__line.bc != 0:
            label += f" \nbc=j{self.__line.bc:.2f}"
        if self.__line.tap != 1:
            label += f" \ntap={self.__line.tap:.2f}:1"
        return label
