from PySide6.QtWidgets import QWidget, QComboBox

from controllers.simulator_controller import ElementEvent, SimulatorController
from models.bus import Bus
from models.connection import BusConnection
from models.network_element import NetworkElement
from view.text_field import TextField


class LineTableRow:

    def __init__(self, line: BusConnection):
        SimulatorController.instance().listen(self.circuitListener)
        self.line = line

        # Field 1: "tap bus" (string)
        self.tapBusField = TextField[str](type=str, enabled=False)

        # Field 2: "z bus" (string)
        self.zBusField = TextField[str](type=str, enabled=False)

        # Field 3: unnamed dropdown (allow user to pick Z or Y)
        self.choiceField = QComboBox()
        self.choiceField.addItems(["Z", "Y"])  # type: ignore
        self.choiceField.currentIndexChanged.connect(self.on_choice_field_updated)

        # Field 4: "r" (float) – using (1/element.y).real if available
        self.resistanceField = TextField[float](type=float, on_focus_out=self.save)

        # Field 5: "x" (float) – using (1/element.y).imag if available
        self.reactanceField = TextField[float](type=float, on_focus_out=self.save)

        # Field 6: "g" (float)
        self.conductanceField = TextField[float](type=float, enabled=False, on_focus_out=self.save)

        # Field 7: "b" (float)
        self.susceptanceField = TextField[float](type=float, enabled=False)

        # Field 8: "bc" (float)
        self.bcField = TextField[float](type=float, on_focus_out=self.save)

        # Field 9: "tap" (float)
        self.tapField = TextField[float](type=float, on_focus_out=self.save)

        self.update_values()

    def get_widgets(self) -> list[QWidget]:
        return [
            self.tapBusField,
            self.zBusField,
            self.choiceField,
            self.resistanceField,
            self.reactanceField,
            self.conductanceField,
            self.susceptanceField,
            self.bcField,
            self.tapField,
        ]

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
            self.line.copyWith(y=y, bc=bc, tap=complex(tap))
        )

    def update_values(self) -> None:
        tap_bus: Bus = SimulatorController.instance().get_bus_by_id(self.line.tap_bus_id)
        z_bus: Bus = SimulatorController.instance().get_bus_by_id(self.line.z_bus_id)
        z: complex = 1 / self.line.y if self.line.y else 0.0
        self.tapBusField.setValue(tap_bus.name)
        self.zBusField.setValue(z_bus.name)
        self.resistanceField.setValue(z.real)
        self.reactanceField.setValue(z.imag)
        self.conductanceField.setValue(self.line.y.real)
        self.susceptanceField.setValue(self.line.y.imag)
        self.bcField.setValue(self.line.bc)
        self.tapField.setValue(self.line.tap.real)

    def circuitListener(self, element: NetworkElement, event: ElementEvent):
        if event is ElementEvent.UPDATED and isinstance(element, BusConnection) and element.id == self.line.id:
            self.line = element
            self.update_values()
            return

        if (
            event is ElementEvent.UPDATED
            and isinstance(element, Bus)
            and element.id in (self.line.tap_bus_id, self.line.z_bus_id)
        ):
            self.update_values()
            return
