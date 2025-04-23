
from typing import *
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
)
from controllers.simulator_controller import ElementEvent, SimulatorController
from PySide6.QtWidgets import QLabel


from models.circuit_element import CircuitElement
from models.transmission_line import TransmissionLineElement


class TransmissionLineTile(QWidget):

    def circuitListener(self, element: CircuitElement, event: ElementEvent):
        if (
            event is ElementEvent.UPDATED
            and element.id == self.line.id
            and isinstance(element, TransmissionLineElement)
        ):
            self.simulatorInstance = SimulatorController.instance()
            self.simulatorInstance.listeners.append(self.circuitListener)
            sourceName = self.simulatorInstance.elements[element.sourceId].name
            targetName = self.simulatorInstance.elements[element.targetId].name
            self.sourceLabel.setText(f"From: {sourceName}, To: {targetName}")
            self.name.setText(element.name)
            self.r.setText(str(element.r))
            self.x.setText(str(element.x))
            self.line = element

    def __init__(self, line: TransmissionLineElement):
        super().__init__()
        self.line: TransmissionLineElement = line

        layout = QVBoxLayout(self)
        title = QLabel("Transmission Line")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        self.simulatorInstance = SimulatorController.instance()
        self.simulatorInstance.listeners.append(self.circuitListener)
        sourceName = self.simulatorInstance.elements[line.sourceId].name
        targetName = self.simulatorInstance.elements[line.targetId].name

        self.sourceLabel = QLabel(f"From: {sourceName}, To: {targetName}")
        layout.addWidget(self.sourceLabel)

        self.name = QLineEdit()
        self.name.setPlaceholderText("Name")
        self.name.setText(line.name)
        layout.addWidget(self.name)

        self.r = QLineEdit()
        self.r.setPlaceholderText("r")
        self.r.setText(str(line.r))
        layout.addWidget(self.r)

        self.x = QLineEdit()
        self.x.setPlaceholderText("x")
        self.x.setText(str(line.x))
        layout.addWidget(self.x)

        def _submit_line_edit():
            copy = self.line.copy()
            copy.name = self.name.text()
            try:
                r = float(self.r.text())
                if r < 0:
                    raise ValueError("r must be positive")
                copy.r = r
                x = float(self.x.text())
                if x < 0:
                    raise ValueError("x must be positive")
                copy.x = x
                SimulatorController.instance().updateElement(copy)
            except ValueError:
                pass

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(_submit_line_edit)
        layout.addWidget(submit_button)


