from typing import *
from PySide6.QtWidgets import (
    QGraphicsLineItem,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen


class LinkLineItem(QGraphicsLineItem):
    def __init__(self, widget1, widget2):
        super().__init__()
        self.widget1 = widget1
        self.widget2 = widget2
        self.setPen(QPen(Qt.black, 2))
        self.setZValue(0)  # So that it stays behind the squares

    def updatePosition(self):
        p1 = self.widget1.sceneBoundingRect().center()
        p2 = self.widget2.sceneBoundingRect().center()
        self.setLine(p1.x(), p1.y(), p2.x(), p2.y())

    def paint(self, painter, option, widget):
        self.updatePosition()
        super().paint(painter, option, widget)
