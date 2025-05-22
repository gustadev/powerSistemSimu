from typing import *
from PySide6.QtWidgets import QHBoxLayout
from controllers.simulator_controller import SimulatorController

from models.bus import Bus
from models.connection import BusConnection
from models.network_element import ElementEvent, NetworkElement
from view.circuit_tiles.components.element_tile import ElementTile
from PySide6.QtWidgets import QComboBox
from view.circuit_tiles.components.text_field import TextField


class LineTile(ElementTile[BusConnection]):

    def __init__(self, element: BusConnection):
        super().__init__(element=element, type=BusConnection)

    def build_form(self, layout: QHBoxLayout):
        super().build_form(layout)

        # Field 1: "tap bus" (string)
        self.tapBusField = TextField[str](type=str, enabled=False)
        layout.addWidget(self.tapBusField)

        # Field 2: "z bus" (string)
        self.zBusField = TextField[str](type=str, enabled=False)
        layout.addWidget(self.zBusField)
        # Field 3: unnamed dropdown (allow user to pick Z or Y)
        self.choiceField = QComboBox()
        self.choiceField.addItems(["Z", "Y"])  # type: ignore
        self.choiceField.currentIndexChanged.connect(self.on_choice_field_updated)
        layout.addWidget(self.choiceField)

        # Field 4: "r" (float) – using (1/element.y).real if available
        self.resistanceField = TextField[float](
            type=float,
            on_focus_out=self.save,
        )
        layout.addWidget(self.resistanceField)

        # Field 5: "x" (float) – using (1/element.y).imag if available
        self.reactanceField = TextField[float](
            type=float,
            on_focus_out=self.save,
        )
        layout.addWidget(self.reactanceField)

        # Field 6: "g" (float)
        self.conductanceField = TextField[float](
            type=float,
            enabled=False,
            default_Value=1.0,
            on_focus_out=self.save,
        )
        layout.addWidget(self.conductanceField)

        # Field 7: "b" (float)
        self.susceptanceField = TextField[float](
            type=float,
            enabled=False,
            default_Value=0.0,
            on_focus_out=self.save,
        )
        layout.addWidget(self.susceptanceField)

        # Field 8: "bc" (float)
        self.bcField = TextField[float](
            type=float,
            default_Value=0.0,
            on_focus_out=self.save,
        )
        layout.addWidget(self.bcField)

        # Field 9: "tap" (float)
        self.tapField = TextField[float](
            type=float,
            default_Value=1.0,
            on_focus_out=self.save,
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
        self.tapBusField.setValue(tap_bus.name)
        self.zBusField.setValue(z_bus.name)
        self.resistanceField.setValue(z.real)
        self.reactanceField.setValue(z.imag)
        self.conductanceField.setValue(self.element.y.real)
        self.susceptanceField.setValue(self.element.y.imag)
        self.bcField.setValue(self.element.bc)
        self.tapField.setValue(self.element.tap.real)

    def validate(self) -> bool:
        return True  # TODO implement validation

    def save(self) -> None:
        y: complex = complex(0)
        if self.choiceField.currentIndex() == 0:
            r = self.resistanceField.getValue()
            x = self.reactanceField.getValue()
            if r is None:
                r = 1.0
            if x is None:
                x = 0.0
            y = 1 / complex(r, x)
            # TODO add validation to prevent inifite Y
        else:
            g = self.conductanceField.getValue()
            b = self.susceptanceField.getValue()
            if g is None:
                g = 1.0
            if b is None:
                b = 0.0
            y = complex(g, b)
        bc = self.bcField.getValue()
        tap = self.tapField.getValue()
        if bc is None:
            bc = 0.0
        if tap is None:
            tap = 1.0

        SimulatorController.instance().updateElement(
            self.element.copyWith(y=y, bc=bc, tap=complex(tap))
        )

    def circuitListener(self, element: NetworkElement, event: ElementEvent):
        super().circuitListener(element, event)
        if (
            event == ElementEvent.UPDATED
            and isinstance(element, Bus)
            and element.id in (self.element.tap_bus_id, self.element.z_bus_id)
        ):
            self.update_form_values()
