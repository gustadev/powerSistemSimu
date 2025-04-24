from typing import *
from PySide6.QtWidgets import (
    QVBoxLayout,
)
from controllers.simulator_controller import SimulatorController


from enums.element_event import ElementEvent
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

        self.conductanceField = TextField[float](
            title="g",
            value=self.element.conductance,
            trailing="S",
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.conductanceField)

        self.susceptanceField = TextField[float](
            title="b",
            value=self.element.susceptance,
            trailing="S",
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.susceptanceField)

        self.busField = TextField(title="bus", type=str, enabled=False)
        layout.addWidget(self.busField)

    def update_form_values(self):
        super().update_form_values()
        self.resistanceField.setValue(self.element.resistance)
        self.reactanceField.setValue(self.element.reactance)
        self.conductanceField.setValue(self.element.conductance)
        self.susceptanceField.setValue(self.element.susceptance)
        self.busField.setValue(
            SimulatorController.instance().getElementNames(
                [self.element.source_id, self.element.target_id]
            )
        )

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
            conductance=self.conductanceField.getValue(),
            susceptance=self.susceptanceField.getValue(),
        )

        SimulatorController.instance().updateElement(copy)

    def circuitListener(self, element, event):
        super().circuitListener(element, event)

        if event == ElementEvent.UPDATED and (
            element.id == self.element.source_id or element.id == self.element.target_id
        ):
            self.update_form_values()
