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

    def addNodeWidget(self, nodeName: string):
        # Add the visual representation
        x = 50
        y = 50
        widget = QGraphicsRectItem(x, y, 50, 50)
        widget.setBrush(Qt.gray)
        widget.setFlag(QGraphicsRectItem.ItemIsMovable, True)
        widget.setFlag(QGraphicsRectItem.ItemIsSelectable, True)
        self.scene().addItem(widget)

        DraggableLinkSquare(
            x + 50 / 2,
            y + 50 / 2,
            nodeName,
            widget,
            onConnectionStart=self.onLinkConnected,
        )

        # Add label
        label = QGraphicsSimpleTextItem(nodeName, parent=widget)
        label.setPos(x + 5, y)

    def onLinkConnected(self, sourceNodeDraggableLink: DraggableLinkSquare, targetNodeDraggableLink: DraggableLinkSquare):
        (canLink,nodeName) = self.onElementLinked(sourceNodeDraggableLink.nodeName, targetNodeDraggableLink.nodeName)
        if canLink:
            self.scene().addItem(LinkLineItem(sourceNodeDraggableLink, targetNodeDraggableLink, nodeName))

    # TODO handle deletion. must sync with simulator state
    # def keyPressEvent(self, event):
    #     if event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
    #         for item in self.scene().selectedItems():
    #             self.scene().removeItem(item)
    #     else:
    #         super().keyPressEvent(event)
