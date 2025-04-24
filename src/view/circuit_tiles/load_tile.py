from typing import *
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
)

from controllers.simulator_controller import SimulatorController

from enums.element_event import ElementEvent
from models.circuit_element import CircuitElement
from models.load import LoadNode
from view.circuit_tiles.tile_field import (
    NotEmptyValidator,
    NumberValidator,
    TextField,
    TitleLabel,
)


class LoadTile(QWidget):
    def __init__(self, node: LoadNode):
        super().__init__()
        self.node: LoadNode = node
        self.simulatorController = SimulatorController.instance()
        self.simulatorController.listen(self.circuitListener)

        layout = QVBoxLayout(self)
        self._pending_title = TitleLabel(self.node.type)
        layout.addWidget(self._pending_title)

        self.nameField = TextField(
            title="name", value=node.name, type=str, validators=[NotEmptyValidator()]
        )
        layout.addWidget(self.nameField)

        self.busField = TextField(
            title="bus",
            value=(
                self.simulatorController.getElementById(node.connection_id).name
                if node.connection_id
                else ""
            ),
            type=str,
            validators=[],
            enabled=False,
        )
        layout.addWidget(self.busField)

        self.powerField = TextField[float](
            title="p set",
            value=node.p_set,
            trailing="kVA",
            type=float,
            validators=[NotEmptyValidator(), NumberValidator(min=0)],
        )
        layout.addWidget(self.powerField)

        def _submit_node_edition():
            for validator in [
                self.nameField.validate,
                self.powerField.validate,
            ]:
                if not validator():
                    return

            copy = self.node.copy()

            copy.name = self.nameField.getValue()
            copy.p_set = self.powerField.getValue()
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
            and isinstance(element, LoadNode)
        ):
            self.nameField.setValue(element.name)
            self.powerField.setValue(element.p_set)
            self.busField.setValue(
                self.simulatorController.getElementById(element.connection_id).name
                if element.connection_id
                else ""
            )
            self.node = element
            return

        if event == ElementEvent.UPDATED and element.id == self.node.connection_id:
            self.busField.setValue(element.name)
            return
