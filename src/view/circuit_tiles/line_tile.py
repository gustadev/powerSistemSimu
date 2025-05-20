from typing import *
from PySide6.QtWidgets import QHBoxLayout
from controllers.simulator_controller import SimulatorController

from models.bus import Bus
from models.connection import BusConnection
from view.circuit_tiles.components.element_tile import ElementTile
from PySide6.QtWidgets import QComboBox
from view.circuit_tiles.components.text_field import (
    NotEmptyValidator,
    NumberValidator,
    TextField,
)


class LineTile(ElementTile[BusConnection]):

    def __init__(self, element: BusConnection):
        super().__init__(element=element, type=BusConnection)

    def build_form(self, layout: QHBoxLayout):
        super().build_form(layout)

        # Field 1: "tap bus" (string)
        self.tapBusField = TextField[int](type=int, validators=[NotEmptyValidator()], enabled=False)
        layout.addWidget(self.tapBusField)

        # Field 2: "z bus" (string)
        self.zBusField = TextField[int](type=int, validators=[NotEmptyValidator()], enabled=False)
        layout.addWidget(self.zBusField)
        # Field 3: unnamed dropdown (allow user to pick Z or Y)
        self.choiceField = QComboBox()
        self.choiceField.addItems(["Z", "Y"])
        self.choiceField.currentIndexChanged.connect(self.on_choice_field_updated)
        layout.addWidget(self.choiceField)

        # Field 4: "r" (float) – using (1/element.y).real if available
        self.resistanceField = TextField[float](
            type=float,
            validators=[NotEmptyValidator(), NumberValidator(min=0)],
        )
        layout.addWidget(self.resistanceField)

        # Field 5: "x" (float) – using (1/element.y).imag if available
        self.reactanceField = TextField[float](
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.reactanceField)

        # Field 6: "g" (float)
        self.conductanceField = TextField[float](
            type=float,
            validators=[NotEmptyValidator(), NumberValidator(min=0)],
            enabled=False,
        )
        layout.addWidget(self.conductanceField)

        # Field 7: "b" (float)
        self.susceptanceField = TextField[float](
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
            enabled=False,
        )
        layout.addWidget(self.susceptanceField)

        # Field 8: "bc" (float)
        self.bcField = TextField[float](
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.bcField)

        # Field 9: "tap" (float)
        self.tapField = TextField[float](
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.tapField)

    def on_choice_field_updated(self, option: int):
        if option == 0:  # Z
            self.resistanceField.setEnabled(True)
            self.reactanceField.setEnabled(True)
            self.conductanceField.setEnabled(False)
            self.susceptanceField.setEnabled(False)
        elif option == 1:  # Y
            self.resistanceField.setEnabled(False)
            self.reactanceField.setEnabled(False)
            self.conductanceField.setEnabled(True)
            self.susceptanceField.setEnabled(True)
        pass

    def update_form_values(self):
        super().update_form_values()
        tap_bus: Bus = SimulatorController.instance().get_bus_by_id(self.element.tap_bus_id)
        z_bus: Bus = SimulatorController.instance().get_bus_by_id(self.element.z_bus_id)
        z: complex = 1 / self.element.y if self.element.y else 0.0
        self.tapBusField.setValue(tap_bus.number)
        self.zBusField.setValue(z_bus.number)
        self.resistanceField.setValue(z.real)
        self.reactanceField.setValue(z.imag)
        self.conductanceField.setValue(self.element.y.real)
        self.susceptanceField.setValue(self.element.y.imag)
        self.bcField.setValue(self.element.bc)
        self.tapField.setValue(self.element.tap.real)

    def edit(self):
        # Validate all fields
        for validator in [
            self.nameField.validate,
            self.tapBusField.validate,
            self.zBusField.validate,
            self.choiceField.validate,
            self.resistanceField.validate,
            self.reactanceField.validate,
            self.conductanceField.validate,
            self.susceptanceField.validate,
            self.bcField.validate,
            self.tapField.validate,
            self.extraField.validate,
        ]:
            if not validator():
                return

        # Create a copy of the element with the updated values
        copy = self.element.copyWith(
            name=self.nameField.getValue(),
            tap_bus=self.tapBusField.getValue(),
            z_bus=self.zBusField.getValue(),
            # The user choice can be handled as needed from choiceField.getValue()
            resistance=self.resistanceField.getValue(),
            reactance=self.reactanceField.getValue(),
            conductance=self.conductanceField.getValue(),
            susceptance=self.susceptanceField.getValue(),
            bc=self.bcField.getValue(),
            tap=self.tapField.getValue(),
            # extraField can be processed if needed
        )

        SimulatorController.instance().updateElement(copy)

    def circuitListener(self, element, event):
        # Optionally update values in response to changes.
        pass
