from typing import *
from PySide6.QtWidgets import QWidget, QVBoxLayout

from controllers.simulator_controller import ElementEvent, SimulatorController


from PySide6.QtCore import Qt
from models.bus import BusNode
from models.circuit_element import CircuitElement
from models.generator import GeneratorNode
from models.load import LoadNode
from models.transmission_line import TransmissionLineElement
from view.circuit_tiles.bus_tile import BusNodeTile
from view.circuit_tiles.generator_tile import GeneratorTile
from view.circuit_tiles.load_tile import LoadTile
from view.circuit_tiles.transmission_line_tile import TransmissionLineTile
from PySide6.QtWidgets import QScrollArea
from PySide6.QtWidgets import QFrame


class ElementList(QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.simulatorInstance = SimulatorController.instance()
        self.simulatorInstance.listen(self.circuitListener)
        self.setLayout(QVBoxLayout())
        self.items = dict()
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        container = QWidget()
        container.setContentsMargins(0, 0, 0, 0)
        self.inner_layout = QVBoxLayout(container)
        self.inner_layout.setAlignment(Qt.AlignTop)
        self.inner_layout.setContentsMargins(0, 0, 0, 0)

        scroll_area.setWidget(container)
        self.layout().addWidget(scroll_area)

    def circuitListener(self, element: CircuitElement, event: ElementEvent):
        if event is ElementEvent.CREATED:
            tile = None
            if isinstance(element, BusNode):
                tile = BusNodeTile(element)

            if isinstance(element, TransmissionLineElement):
                tile = TransmissionLineTile(element)

            if isinstance(element, LoadNode):
                tile = LoadTile(element)

            if isinstance(element, GeneratorNode):
                tile = GeneratorTile(element)

            if tile:
                self.inner_layout.addWidget(tile)
                card = QFrame()
                card.setFrameShape(QFrame.StyledPanel)
                card.setFrameShadow(QFrame.Raised)
                card_layout = QVBoxLayout(card)
                card_layout.setContentsMargins(8, 8, 8, 8)
                card_layout.addWidget(tile)
                self.inner_layout.addWidget(card)
                self.items[element.id] = tile
