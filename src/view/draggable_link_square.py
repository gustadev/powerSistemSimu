import string
from typing import *
from PySide6.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsLineItem,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen

from controllers.simulator_controller import SimulatorController


class DraggableLinkSquare(QGraphicsRectItem):
    def __init__(self, x, y, parent: QGraphicsRectItem):
        super().__init__(x, y, 10, 10, parent=parent)
        self.parent = parent
        self.setBrush(Qt.GlobalColor.red)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsFocusable, True)
        self.drag_line = None

    def mousePressEvent(self, event):
        self.startPos = event.scenePos()
        event.accept()

    def mouseMoveEvent(self, event):
        if not self.drag_line:
            self.drag_line = QGraphicsLineItem()
            self.drag_line.setPen(QPen(Qt.GlobalColor.blue, 2, Qt.PenStyle.DashLine))
            self.scene().addItem(self.drag_line)
        self.drag_line.setLine(
            self.startPos.x(),
            self.startPos.y(),
            event.scenePos().x(),
            event.scenePos().y(),
        )
        event.accept()

    def mouseReleaseEvent(self, event):
        if self.drag_line:
            self.scene().removeItem(self.drag_line)
            self.drag_line = None

        items = self.scene().items(event.scenePos())
        target = None
        for item in items:
            if (
                item is not self
                and isinstance(item, DraggableLinkSquare)
                and item.parentItem() != self.parentItem()
            ):
                target = item
            break
        if target:
            SimulatorController.instance().addConnection(self.parent.node, target.parent.node)
        event.accept()
