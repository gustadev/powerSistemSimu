from typing import Tuple
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
from storage.storage import StorageFacade
from view.bus_widget import BusWidget
from view.link_line_item import LinkLineItem
from PySide6.QtWidgets import QFileDialog


class BoardView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setBackgroundBrush(Qt.GlobalColor.white)

        # self.setSceneRect(0, 0, 600, 400)
        self.simulator_widgets = dict[str, object]()
        simulatorInstance = SimulatorController.instance()
        simulatorInstance.listen(self.circuitListener)
    
     # Variáveis para panning
        self._panning = False
        self._pan_start = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self._panning = True
            self._pan_start = event.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._panning and self._pan_start:
            delta = event.pos() - self._pan_start
            self._pan_start = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self._panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)

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

    def import_ieee(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import IEEE File", "", "IEEE Files (*.txt);;All Files (*)"
        )
        if not file_path:
            return
        SimulatorController.instance().clear_state()

        try:
            power_flow = StorageFacade.read_ieee_file(file_path)
            for bus in power_flow.buses.values():
                SimulatorController.instance().addBus(bus)
            for line in power_flow.connections.values():
                SimulatorController.instance().addConnection(line)

        except Exception as e:
            print(f"Error importing IEEE file: {e}")
        pass

    def import_json(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import JSON File", "", "JSON Files (*.json);;All Files (*)"
        )
        if not file_path:
            return

        SimulatorController.instance().clear_state()
        try:
            buses, lines, positions = StorageFacade.read_json_file(file_path)
            for bus in buses:
                SimulatorController.instance().addBus(bus)
            for line in lines:
                SimulatorController.instance().addConnection(line)

            for index, bus in enumerate(buses):
                bus_widget = self.simulator_widgets[bus.id]
                position = positions[index]
                bus_widget.setPos(position[0], position[1])
        except Exception as e:
            print(f"Error importing JSON file: {e}")

    def export_json(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export to JSON", "", "JSON Files (*.json);;All Files (*)"
        )
        if not file_path:
            return

        positions = list[Tuple[float, float]]()
        for element in self.simulator_widgets.values():
            if isinstance(element, BusWidget):
                positions.append((element.x(), element.y()))
        StorageFacade.save_json_file(
            file_path,
            buses=SimulatorController.instance().buses,
            lines=SimulatorController.instance().connections,
            positions=positions,
        )

    # TODO handle deletion. must sync with simulator state
    # def keyPressEvent(self, event):
    #     if event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
    #         for item in self.scene().selectedItems():
    #             self.scene().removeItem(item)
    #     else:
    #         super().keyPressEvent(event)
