from typing import *
from PySide6.QtWidgets import (
    QVBoxLayout,
)
from controllers.simulator_controller import SimulatorController


from models.connection import BusConnection
from view.circuit_tiles.components.element_tile import ElementTile
from view.circuit_tiles.components.text_field import (
    NotEmptyValidator,
    NumberValidator,
    TextField,
)


class LineTile(ElementTile[BusConnection]):

    def __init__(self, element: BusConnection):
        super().__init__(element=element, type=BusConnection)

    def build_form(self, layout: QVBoxLayout):
        super().build_form(layout)
        self.resistanceField = TextField[float](
            title="r",
            value=(1 / self.element.y).real,
            trailing="Ohm",
            type=float,
            validators=[NotEmptyValidator(), NumberValidator(min=0)],
        )
        layout.addWidget(self.resistanceField)

        self.reactanceField = TextField[float](
            title="x",
            value=(1 / self.element.y).imag,
            trailing="Ohm",
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
        )

        layout.addWidget(self.reactanceField)

        # self.busField = TextField(title="bus", type=str, enabled=False)
        # layout.addWidget(self.busField)

    def update_form_values(self):
        super().update_form_values()
        # self.resistanceField.setValue(self.element.resistance)
        # self.reactanceField.setValue(self.element.reactance)
        # self.conductanceField.setValue(self.element.conductance)
        # self.susceptanceField.setValue(self.element.susceptance)
        # self.busField.setValue(
        #     SimulatorController.instance().getElementNames(
        #         [self.element.source_id, self.element.target_id]
        #     )
        # )

    def edit(self):
        for validator in [
            self.nameField.validate,
            self.resistanceField.validate,
            self.reactanceField.validate,
        ]:
            if not validator():
                return

        # copy = self.element.copyWith(
        #     name=self.nameField.getValue(),
        #     resistance=self.resistanceField.getValue(),
        #     reactance=self.reactanceField.getValue(),
        #     conductance=self.conductanceField.getValue(),
        #     susceptance=self.susceptanceField.getValue(),
        # )

        # SimulatorController.instance().updateElement(copy)

    def circuitListener(self, element, event):
        # super().circuitListener(element, event)

        # if event == ElementEvent.UPDATED and (
        #     element.id == self.element.source_id or element.id == self.element.target_id
        # ):
        #     self.update_form_values()
        pass
