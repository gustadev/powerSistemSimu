from typing import *
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
)
from controllers.simulator_controller import ElementEvent, SimulatorController
from PySide6.QtWidgets import QLabel


from models.bus import BusNode
from models.circuit_element import CircuitElement
from models.transmission_line import TransmissionLineElement
from view.circuit_tiles.tile_field import (
    NotEmptyValidator,
    NumberValidator,
    TextField,
    TitleLabel,
)


class TransmissionLineTile(QWidget):

    def __init__(self, line: TransmissionLineElement):
        super().__init__()
        self.line: TransmissionLineElement = line

        layout = QVBoxLayout(self)
        self._pending_title = TitleLabel(self.line.type)
        layout.addWidget(self._pending_title)

        self.simulatorInstance = SimulatorController.instance()
        self.simulatorInstance.listen(self.circuitListener)
        sourceName = self.simulatorInstance.getElementById(line.source_id).name
        targetName = self.simulatorInstance.getElementById(line.target_id).name

        self.sourceLabel = QLabel(f"From: {sourceName}, To: {targetName}")
        layout.addWidget(self.sourceLabel)

        self.nameField = TextField(
            title="name", value=line.name, type=str, validators=[NotEmptyValidator()]
        )
        layout.addWidget(self.nameField)

        self.resistanceField = TextField[float](
            title="r",
            value=line.resistance,
            trailing="ohm",
            type=float,
            validators=[NotEmptyValidator(), NumberValidator(min=0)],
        )
        layout.addWidget(self.resistanceField)

        self.reactanceField = TextField[float](
            title="x",
            value=line.reactance,
            trailing="ohm",
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.reactanceField)

        def _submit_line_edit():
            for validator in [
                self.nameField.validate,
                self.resistanceField.validate,
                self.reactanceField.validate,
            ]:
                if not validator():
                    return

            copy = self.line.copy()
            copy.name = self.nameField.getValue()
            copy.resistance = self.resistanceField.getValue()
            copy.reactance = self.reactanceField.getValue()
            SimulatorController.instance().updateElement(copy)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(_submit_line_edit)
        layout.addWidget(submit_button)

    def circuitListener(self, element: CircuitElement, event: ElementEvent):
        if (
            event is ElementEvent.UPDATED
            and element.id == self.line.id
            and isinstance(element, TransmissionLineElement)
        ):
            sourceName = self.simulatorInstance.getElementById(element.source_id).name
            targetName = self.simulatorInstance.getElementById(element.target_id).name
            self.sourceLabel.setText(f"From: {sourceName}, To: {targetName}")
            self.nameField.setValue(element.name)
            self.resistanceField.setValue(element.resistance)
            self.reactanceField.setValue(element.reactance)
            self.line = element
            return

        if (
            event is ElementEvent.UPDATED
            and isinstance(element, BusNode)
            and element.id == self.line.source_id
        ):
            self.sourceLabel.setText(
                f"From: {element.name}, To: {self.simulatorInstance.getElementById(self.line.target_id).name}"
            )
            return

        if (
            event is ElementEvent.UPDATED
            and isinstance(element, BusNode)
            and element.id == self.line.target_id
        ):

            self.sourceLabel.setText(
                f"From: {self.simulatorInstance.getElementById(self.line.source_id).name}, To: {element.name}"
            )
            return
