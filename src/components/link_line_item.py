from typing import *
from PySide6.QtWidgets import (
    QGraphicsLineItem,
)
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsSimpleTextItem
from PySide6.QtGui import QPen


class LinkLineItem(QGraphicsLineItem):
    def __init__(
        self, sourceNodeDraggableLink, targetNodeDraggableLink, connectionName
    ):
        super().__init__()
        self.sourceNodeDraggableLink = sourceNodeDraggableLink
        self.targetNodeDraggableLink = targetNodeDraggableLink
        self.setPen(QPen(Qt.blue, 1))
        self.setZValue(0)  # So that it stays behind the squares
        self.connectionName = None
        self.center = None
        if connectionName:
            self.connectionName = QGraphicsSimpleTextItem(connectionName)
            self.connectionName.setBrush(Qt.white)
            self.connectionName.setParentItem(self)

    def updatePosition(self):
        p1 = self.sourceNodeDraggableLink.sceneBoundingRect().center()
        p2 = self.targetNodeDraggableLink.sceneBoundingRect().center()
        self.setLine(p1.x(), p1.y(), p2.x(), p2.y())
        if self.connectionName:
            self.center = p1 + (p2 - p1) / 2
            self.connectionName.setPos(self.center.x(), self.center.y())

    def paint(self, painter, option, widget):
        self.updatePosition()
        super().paint(painter, option, widget)
