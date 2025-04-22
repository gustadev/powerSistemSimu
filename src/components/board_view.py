from typing import *
from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
)
from PySide6.QtGui import QPainter

from components.circuit_node_widget import CircuitNodeWidget
from components.link_line_item import LinkLineItem
from models.circuit_node import CircuitNode, TransmissionLineNode
from models.simulator_state import SimulatorState


class BoardView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        self.setSceneRect(0, 0, 600, 400)
        self.simulatorWidgets = dict()
        simulatorInstance = SimulatorState.instance()
        simulatorInstance.onNodeCreated = self.addNodeWidget
        simulatorInstance.onWireCreated = self.addConnectionWidget

    def addNodeWidget(self, node: CircuitNode):
        widget = CircuitNodeWidget(50, 50, node)
        self.scene().addItem(widget)
        self.simulatorWidgets[node.id] = widget

    def addConnectionWidget(
        self,
        sourceNode: CircuitNode,
        targetNode: CircuitNode,
        line: TransmissionLineNode | None,
    ):
        sourceWidget = self.simulatorWidgets[sourceNode.id].link
        targetWidget = self.simulatorWidgets[targetNode.id].link
        self.scene().addItem(LinkLineItem(sourceWidget, targetWidget, line))

    # TODO handle deletion. must sync with simulator state
    # def keyPressEvent(self, event):
    #     if event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
    #         for item in self.scene().selectedItems():
    #             self.scene().removeItem(item)
    #     else:
    #         super().keyPressEvent(event)
