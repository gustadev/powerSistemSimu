from typing import *
from PySide6.QtWidgets import QVBoxLayout

from controllers.simulator_controller import SimulatorController

from enums.element_event import ElementEvent
from models.bus import BusNode
from view.circuit_tiles.components.element_tile import ElementTile
from view.circuit_tiles.components.text_field import (
    NotEmptyValidator,
    NumberValidator,
    TextField,
)


class BusNodeTile(ElementTile[BusNode]):
    def __init__(self, element: BusNode):
        super().__init__(element=element, type=BusNode)

    def build_form(self, layout: QVBoxLayout):
        super().build_form(layout)
        self.voltageField = TextField[float](
            title="v_nom",
            trailing="kV",
            type=float,
            validators=[NotEmptyValidator(), NumberValidator(min=0)],
        )
        layout.addWidget(self.voltageField)

        self.connectionsField = TextField[str](
            title="nodes",
            type=str,
            enabled=False,
        )
        layout.addWidget(self.connectionsField)

    def update_form_values(self):
        super().update_form_values()
        self.voltageField.setValue(self.element.v_nom)
        self.connectionsField.setValue(
            SimulatorController.instance().getElementNames(self.element.connection_ids)
        )
        return

    def edit(self):
        for validator in [self.nameField.validate, self.voltageField.validate]:
            if not validator():
                return

        copy = self.element.copyWith(
            name=self.nameField.getValue(), v_nom=self.voltageField.getValue()
        )

        SimulatorController.instance().updateElement(copy)

    def circuitListener(self, element: BusNode, event: ElementEvent):
        super().circuitListener(element, event)

        if event == ElementEvent.UPDATED and element.id in self.element.connection_ids:
            self.update_form_values()
