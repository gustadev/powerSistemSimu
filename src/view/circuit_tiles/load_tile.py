from typing import *
from PySide6.QtWidgets import (
    QVBoxLayout,
)

from controllers.simulator_controller import SimulatorController

from models.load import LoadNode
from view.circuit_tiles.components.element_tile import ElementTile
from view.circuit_tiles.components.text_field import (
    NotEmptyValidator,
    NumberValidator,
    TextField,
)


class LoadTile(ElementTile[LoadNode]):
    def __init__(self, element: LoadNode):
        super().__init__(element=element, type=LoadNode)

    def build_form(self, layout: QVBoxLayout):
        super().build_form(layout)
        self.powerField = TextField[float](
            title="p set",
            trailing="kVA",
            type=float,
            validators=[NotEmptyValidator(), NumberValidator(min=0)],
        )
        layout.addWidget(self.powerField)

    def update_form_values(self):
        super().update_form_values()
        self.powerField.setValue(self.element.p_set)

    def edit(self):
        for validator in [
            self.nameField.validate,
            self.powerField.validate,
        ]:
            if not validator():
                return

        copy = self.element.copyWith(
            name=self.nameField.getValue(), p_set=self.powerField.getValue()
        )

        SimulatorController.instance().updateElement(copy)
