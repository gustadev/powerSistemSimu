from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
from PySide6.QtCore import Qt

from controllers.simulator_controller import ElementEvent, SimulatorController
from models.connection import BusConnection
from models.network_element import NetworkElement
from view.circuit_tiles.line_tile import LineTile


class LineList(QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.simulatorInstance = SimulatorController.instance()
        self.simulatorInstance.listen(self.circuitListener)
        self.setLayout(QVBoxLayout())
        self.items = dict[int, LineTile]()

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        container = QWidget()
        container.setContentsMargins(0, 0, 0, 0)
        self.inner_layout = QVBoxLayout(container)
        self.inner_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.inner_layout.setContentsMargins(2, 2, 2, 2)
        self.inner_layout.setSpacing(0)

        # Add header to the scrollable list with updated field names
        header_frame = QFrame()
        header_frame.setFrameShape(QFrame.StyledPanel)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(8, 8, 8, 8)

        fields = [
            "tap bus",
            "z bus",
            "",
            "r",
            "x",
            "g",
            "b",
            "bc",
            "tap",
        ]
        for field in fields:
            header_layout.addWidget(QLabel(field))
        self.inner_layout.addWidget(header_frame)

        scroll_area.setWidget(container)
        self.layout().addWidget(scroll_area)

    def circuitListener(self, element: NetworkElement, event: ElementEvent):
        if event is ElementEvent.CREATED:
            tile = None

            if isinstance(element, BusConnection):
                tile = LineTile(element)

            if tile:
                card = QFrame()
                card.setFrameShape(QFrame.StyledPanel)
                card.setFrameShadow(QFrame.Raised)
                card_layout = QVBoxLayout(card)
                card_layout.setContentsMargins(8, 8, 8, 8)
                card_layout.addWidget(tile)
                self.inner_layout.addWidget(card)
                self.items[element.id] = tile
