from typing import *
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
)

from controllers.simulator_controller import ElementEvent, SimulatorController

from models.bus import BusNode
from models.circuit_element import CircuitElement
from view.circuit_tiles.tile_field import (
    NotEmptyValidator,
    NumberValidator,
    TextField,
    TitleLabel,
)


class BusNodeTile(QWidget):
    def __init__(self, node: BusNode):
        super().__init__()
        self.node: BusNode = node

        layout = QVBoxLayout(self)
        self._pending_title = TitleLabel(self.node.type)
        layout.addWidget(self._pending_title)

        self.nameField = TextField(
            title="name", value=node.name, type=str, validators=[NotEmptyValidator()]
        )
        layout.addWidget(self.nameField)

        self.voltageField = TextField[float](
            title="v nom",
            value=node.v_nom,
            trailing="kV",
            type=float,
            validators=[NotEmptyValidator(), NumberValidator(min=0)],
        )
        layout.addWidget(self.voltageField)

        def _submit_node_edition():
            for validator in [self.nameField.validate, self.voltageField.validate]:
                if not validator():
                    return

            copy = self.node.copy()

            copy.name = self.nameField.getValue()
            copy.v_nom = self.voltageField.getValue()
            SimulatorController.instance().updateElement(copy)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(_submit_node_edition)
        layout.addWidget(self.submit_button)
        simulatorInstance = SimulatorController.instance()
        simulatorInstance.listen(self.circuitListener)

    def circuitListener(self, element: CircuitElement, event: ElementEvent):
        if (
            event is ElementEvent.UPDATED
            and element.id == self.node.id
            and isinstance(element, BusNode)
        ):
            self.node = element
            self.nameField.setValue(element.name)
            self.voltageField.setValue(str(element.v_nom))
