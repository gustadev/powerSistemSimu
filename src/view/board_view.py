from typing import *
from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
)
from PySide6.QtGui import QPainter,Qt

from controllers.simulator_controller import ElementEvent, SimulatorController
from models.circuit_element import CircuitElement, DoubleConnectionElement
from view.circuit_node_widget import CircuitNodeWidget
from view.link_line_item import LinkLineItem


class BoardView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setBackgroundBrush(Qt.GlobalColor.white)
        
        # self.setSceneRect(0, 0, 600, 400)
        self.simulatorWidgets = dict()
        simulatorInstance = SimulatorController.instance()
        simulatorInstance.listen(self.circuitListener)

    # Listens to the simulator events and updates the board
    def circuitListener(self, element: CircuitElement, event: ElementEvent):
        # Adds node component to the board
        if event is ElementEvent.CREATED and not isinstance(
            element, DoubleConnectionElement
        ):
            widget = CircuitNodeWidget(50, 50, element)
            self.scene().addItem(widget)
            self.simulatorWidgets[element.id] = widget
            return

        # Adds line between two components in the board
        # TODO bug: somethimes not creating wire or TL when there is a block selected
        if event is ElementEvent.CREATED and isinstance(
            element, DoubleConnectionElement
        ):
            sourceWidget = self.simulatorWidgets[element.source_id].link
            targetWidget = self.simulatorWidgets[element.target_id].link
            self.scene().addItem(LinkLineItem(sourceWidget, targetWidget, element))
            return

    # TODO handle deletion. must sync with simulator state
    # def keyPressEvent(self, event):
    #     if event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
    #         for item in self.scene().selectedItems():
    #             self.scene().removeItem(item)
    #     else:
    #         super().keyPressEvent(event)
