from typing import *
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
)

from controllers.simulator_controller import SimulatorController

from enums.element_event import ElementEvent
from models.circuit_element import CircuitElement
from models.generator import GeneratorNode
from view.circuit_tiles.tile_field import (
    NotEmptyValidator,
    NumberValidator,
    TextField,
    TitleLabel,
)


class GeneratorTile(QWidget):
    def __init__(self, node: GeneratorNode):
        super().__init__()
        self.node: GeneratorNode = node
        self.simulatorController = SimulatorController.instance()
        self.simulatorController.listen(self.circuitListener)

        layout = QVBoxLayout(self)
        self._pending_title = TitleLabel(self.node.type)
        layout.addWidget(self._pending_title)

        self.nameField = TextField(
            title="name", value=node.name, type=str, validators=[NotEmptyValidator()]
        )
        layout.addWidget(self.nameField)
        self.controlField = TextField(
            title="control",
            value=node.control,
            type=str,
            validators=[NotEmptyValidator()],
        )
        layout.addWidget(self.controlField)

        self.busField = TextField(
            title="bus",
            value=(
                self.simulatorController.getElementById(node.getBusId()).name
                if node.getBusId()
                else ""
            ),
            type=str,
            validators=[],
            enabled=False,
        )
        layout.addWidget(self.busField)

        self.powerField = TextField[float](
            title="power",
            value=node.nominalPower,
            trailing="kVA",
            type=float,
            validators=[NotEmptyValidator(), NumberValidator(min=0)],
        )
        layout.addWidget(self.powerField)

        def _submit_node_edition():
            for validator in [
                self.nameField.validate,
                self.controlField.validate,
                self.powerField.validate,
            ]:
                if not validator():
                    return

            copy = self.node.copy()

            copy.name = self.nameField.getValue()
            copy.nominalPower = self.powerField.getValue()
            copy.control = self.controlField.getValue()
            self.simulatorController.updateElement(copy)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(_submit_node_edition)
        layout.addWidget(self.submit_button)
        simulatorInstance = SimulatorController.instance()
        simulatorInstance.listen(self.circuitListener)

    def circuitListener(self, element: CircuitElement, event: ElementEvent):
        if (
            event == ElementEvent.UPDATED
            and element.id == self.node.id
            and isinstance(element, GeneratorNode)
        ):
            self.nameField.setValue(element.name)
            self.powerField.setValue(element.nominalPower)
            self.controlField.setValue(element.control)
            self.busField.setValue(
                self.simulatorController.getElementById(element.getBusId()).name
                if element.getBusId()
                else ""
            )
            self.node = element
            return

        if event == ElementEvent.UPDATED and element.id == self.node.getBusId():
            self.busField.setValue(element.name)
            return
