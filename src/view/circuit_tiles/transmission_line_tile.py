from typing import *
from PySide6.QtWidgets import (
    QVBoxLayout,
)
from controllers.simulator_controller import SimulatorController


from models.transmission_line import TransmissionLineElement
from view.circuit_tiles.components.element_tile import ElementTile
from view.circuit_tiles.components.text_field import (
    NotEmptyValidator,
    NumberValidator,
    TextField,
)


class TransmissionLineTile(ElementTile[TransmissionLineElement]):

    def __init__(self, element: TransmissionLineElement):
        super().__init__(element=element, type=TransmissionLineElement)

    def build_form(self, layout: QVBoxLayout):
        super().build_form(layout)
        self.resistanceField = TextField[float](
            title="r",
            value=self.element.resistance,
            trailing="ohm",
            type=float,
            validators=[NotEmptyValidator(), NumberValidator(min=0)],
        )
        layout.addWidget(self.resistanceField)

        self.reactanceField = TextField[float](
            title="x",
            value=self.element.reactance,
            trailing="ohm",
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.reactanceField)

    def update_form_values(self):
        super().update_form_values()
        self.resistanceField.setValue(self.element.resistance)
        self.reactanceField.setValue(self.element.reactance)

    def edit(self):
        for validator in [
            self.nameField.validate,
            self.resistanceField.validate,
            self.reactanceField.validate,
        ]:
            if not validator():
                return

        copy = self.element.copyWith(
            name=self.nameField.getValue(),
            resistance=self.resistanceField.getValue(),
            reactance=self.reactanceField.getValue(),
        )

        SimulatorController.instance().updateElement(copy)
