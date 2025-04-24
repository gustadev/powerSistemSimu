from typing import *
from PySide6.QtWidgets import (
    QVBoxLayout,
)

from controllers.simulator_controller import SimulatorController

from enums.element_event import ElementEvent
from models.generator import GeneratorNode
from view.circuit_tiles.components.element_tile import ElementTile
from view.circuit_tiles.components.text_field import (
    NotEmptyValidator,
    NumberValidator,
    TextField,
)


class GeneratorTile(ElementTile[GeneratorNode]):
    def __init__(self, element: GeneratorNode):
        super().__init__(element=element, type=GeneratorNode)

    def build_form(self, layout: QVBoxLayout):
        super().build_form(layout)
        self.controlField = TextField(
            title="control",
            type=str,
            validators=[NotEmptyValidator()],
        )
        layout.addWidget(self.controlField)

        self.powerField = TextField[float](
            title="power",
            trailing="kVA",
            type=float,
            validators=[NotEmptyValidator(), NumberValidator(min=0)],
        )
        layout.addWidget(self.powerField)

        self.busField = TextField(
            title="bus",
            type=str,
            enabled=False,
        )
        layout.addWidget(self.busField)

    def update_form_values(self):
        super().update_form_values()
        self.controlField.setValue(self.element.control)
        self.busField.setValue(
            SimulatorController.instance().getElementNames([self.element.connection_id])
        )
        self.powerField.setValue(self.element.nominal_power)

    def edit(self):
        for validator in [
            self.nameField.validate,
            self.controlField.validate,
            self.powerField.validate,
        ]:
            if not validator():
                return

        copy = self.element.copyWith(
            name=self.nameField.getValue(),
            control=self.controlField.getValue(),
            nominal_power=self.powerField.getValue(),
        )

        SimulatorController.instance().updateElement(copy)

    def circuitListener(self, element, event):
        super().circuitListener(element, event)

        if event == ElementEvent.UPDATED and element.id == self.element.connection_id:
            self.update_form_values()
