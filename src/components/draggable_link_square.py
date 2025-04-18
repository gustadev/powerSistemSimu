import string
from typing import *
from PySide6.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsLineItem,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen


class DraggableLinkSquare(QGraphicsRectItem):
    def __init__(self, x, y, element: string, parentSquare: QGraphicsRectItem, board):
        super().__init__(x, y, 10, 10, parent=parentSquare)
        self.element = element
        self.board = board
        self.setBrush(Qt.red)
        self.setFlag(QGraphicsRectItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsRectItem.ItemIsFocusable, True)
        self.drag_line = None

    def mousePressEvent(self, event):
        self.startPos = event.scenePos()
        event.accept()

    def mouseMoveEvent(self, event):
        if not self.drag_line:
            self.drag_line = QGraphicsLineItem()
            self.drag_line.setPen(QPen(Qt.blue, 2, Qt.DashLine))
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

        # Procura por um item alvo na cena que não seja o próprio botão
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
            self.board.onLinkConnected(self, target)
        event.accept()
