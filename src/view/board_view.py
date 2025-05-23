from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
)
from PySide6.QtGui import QPainter, Qt
from PySide6.QtCore import QRectF

from controllers.simulator_controller import ElementEvent, SimulatorController
from models.bus import Bus
from models.line import Line
from models.network_element import NetworkElement
from view.bus_widget import BusWidget
from view.link_line_item import LinkLineItem


class BoardView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setBackgroundBrush(Qt.GlobalColor.white)

        # self.setSceneRect(0, 0, 600, 400)
        self.simulator_widgets = dict()
        simulatorInstance = SimulatorController.instance()
        simulatorInstance.listen(self.circuitListener)

    def drawBackground(self, painter: QPainter, rect: QRectF):
        painter.setPen(Qt.GlobalColor.lightGray)
        super().drawBackground(painter, rect)

        # Define grid spacing
        gridSize = 20

        # Get the visible area of the scene
        left = int(rect.left()) - (int(rect.left()) % gridSize)
        top = int(rect.top()) - (int(rect.top()) % gridSize)

        # Draw vertical lines
        for x in range(left, int(rect.right()), gridSize):
            painter.drawLine(x, rect.top(), x, rect.bottom())

        # Draw horizontal lines
        for y in range(top, int(rect.bottom()), gridSize):
            painter.drawLine(rect.left(), y, rect.right(), y)

    # Listens to the simulator events and updates the board
    def circuitListener(self, element: NetworkElement, event: ElementEvent):
        # Adds node component to the board
        if event is ElementEvent.CREATED and isinstance(element, Bus):
            widget = BusWidget(50, 50, element)
            self.scene().addItem(widget)
            self.simulator_widgets[element.id] = widget
            return

        # Adds line between two components in the board
        # TODO bug: somethimes not creating wire or TL when there is a block selected
        if event is ElementEvent.CREATED and isinstance(element, Line):
            sourceWidget = self.simulator_widgets[element.tap_bus_id].link
            targetWidget = self.simulator_widgets[element.z_bus_id].link
            line = LinkLineItem(sourceWidget, targetWidget, element)
            self.scene().addItem(line)
            self.simulator_widgets[element.id] = line
            return

        if event is ElementEvent.DELETED:
            widget = self.simulator_widgets[element.id]
            self.scene().removeItem(widget)
            del self.simulator_widgets[element.id]
            return

    # TODO handle deletion. must sync with simulator state
    # def keyPressEvent(self, event):
    #     if event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
    #         for item in self.scene().selectedItems():
    #             self.scene().removeItem(item)
    #     else:
    #         super().keyPressEvent(event)
