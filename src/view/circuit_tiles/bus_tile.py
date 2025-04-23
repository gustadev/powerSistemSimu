from typing import *
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
)

from controllers.simulator_controller import ElementEvent, SimulatorController
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer

from models.bus import BusNode
from models.circuit_element import CircuitElement


class BusNodeTile(QWidget):
    def __init__(self, node: BusNode):
        super().__init__()
        self.node: BusNode = node

        self._pending_title = QLabel(self.node.type)
        self._pending_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        QTimer.singleShot(0, lambda: self.layout().insertWidget(0, self._pending_title))

        layout = QVBoxLayout(self)
        self.nameField = QLineEdit()
        self.nameField.setPlaceholderText("Name")
        self.nameField.setText(node.name)
        layout.addWidget(self.nameField)

        self.voltageField = QLineEdit()
        self.voltageField.setPlaceholderText("Voltage")
        self.voltageField.setText(str(node.v_nom))
        layout.addWidget(self.voltageField)

        def _submit_node_edition():
            copy = self.node.copy()
            copy.name = self.nameField.text()
            try:
                v_nom = float(self.voltageField.text())
                if v_nom < 0:
                    raise ValueError("Voltage must be positive")
                self.node.v_nom = v_nom
                SimulatorController.instance().updateElement(copy)
            except ValueError:
                pass

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(_submit_node_edition)
        layout.addWidget(self.submit_button)
        simulatorInstance = SimulatorController.instance()
        simulatorInstance.listeners.append(self.circuitListener)

    def circuitListener(self, element: CircuitElement, event: ElementEvent):
        if (
            event is ElementEvent.UPDATED
            and element.id == self.node.id
            and isinstance(element, BusNode)
        ):
            self.node = element
            self.nameField.setText(element.name)
            self.voltageField.setText(str(element.v_nom))
