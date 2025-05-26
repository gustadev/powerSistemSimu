from cmath import pi
from PySide6.QtWidgets import QWidget, QComboBox

from controllers.simulator_controller import ElementEvent, SimulatorController
from models.bus import Bus, BusType
from models.network_element import NetworkElement
from view.text_field import TextField


class BusTableRow:
    __degToRad = pi / 180.0
    __radToDeg = 180.0 / pi

    def __init__(self, bus: Bus):
        SimulatorController.instance().listen(self.circuit_listener)
        self.bus = bus

        # "name"
        self.nameField = TextField(type=str, on_focus_out=self.save)

        # "number"
        self.numberField = TextField[int](type=int, on_focus_out=self.save)

        # "type" - using dropdown
        self.busTypeDropdown = QComboBox()
        self.busTypeDropdown.addItems(["SLACK", "PV", "PQ"])
        self.busTypeDropdown.currentIndexChanged.connect(self.save)

        # "v"
        self.voltageField = TextField[float](type=float, on_focus_out=self.save)

        # "o" (angle)
        self.angleField = TextField[float](type=float, on_focus_out=self.save)

        # "p" (read-only field)
        self.p_field = TextField[float](type=float, enabled=False)

        # "q" (read-only field)
        self.q_field = TextField[float](type=float, enabled=False)

        # "p_load"
        self.p_load = TextField[float](type=float, on_focus_out=self.save)

        # "q_load"
        self.q_load = TextField[float](type=float, on_focus_out=self.save)

        # "p_gen"
        self.p_gen = TextField[float](type=float, on_focus_out=self.save)

        # "q_gen"
        self.q_gen = TextField[float](type=float, on_focus_out=self.save)

        # "q_min"
        self.q_min = TextField[float](type=float, on_focus_out=self.save)

        # "q_max"
        self.q_max = TextField[float](type=float, on_focus_out=self.save)

        # "shunt_b"
        self.shunt_b = TextField[float](type=float, on_focus_out=self.save)

        # "shunt_g"
        self.shunt_g = TextField[float](type=float, on_focus_out=self.save)

        self.update_values()

    def get_widgets(self) -> list[QWidget]:
        return [
            self.nameField,
            self.numberField,
            self.busTypeDropdown,
            self.voltageField,
            self.angleField,
            self.p_field,
            self.q_field,
            self.p_load,
            self.q_load,
            self.p_gen,
            self.q_gen,
            self.q_min,
            self.q_max,
            self.shunt_b,
            self.shunt_g,
        ]

    def save(self) -> None:
        bus_type: BusType = BusType[self.busTypeDropdown.currentText()]

        o_from_field: float | None = self.angleField.getValue()
        if o_from_field is not None:
            o_from_field *= BusTableRow.__degToRad

        SimulatorController.instance().updateElement(
            self.bus.copy_with(
                name=self.nameField.getValue(),
                number=self.numberField.getValue(),
                type=bus_type,
                v=self.voltageField.getValue(),
                o=o_from_field,
                p_load=self.p_load.getValue(),
                q_load=self.q_load.getValue(),
                p_gen=self.p_gen.getValue(),
                q_gen=self.q_gen.getValue(),
                q_min=self.q_min.getValue(),
                q_max=self.q_max.getValue(),
                g_shunt=self.shunt_g.getValue(),
                b_shunt=self.shunt_b.getValue(),
            )
        )

    def update_values(self) -> None:
        self.nameField.setValue(self.bus.name)
        self.numberField.setValue(self.bus.number)
        idx = self.busTypeDropdown.findText(self.bus.type.name)
        if idx >= 0:
            self.busTypeDropdown.setCurrentIndex(idx)
        self.voltageField.setValue(self.bus.v)
        self.angleField.setValue(self.bus.o * BusTableRow.__radToDeg)
        self.p_field.setValue(self.bus.p)
        self.q_field.setValue(self.bus.q)
        if self.bus.p_load != 0:
            self.p_load.setValue(self.bus.p_load)
        else:
            self.p_load.clearValue()
        if self.bus.q_load != 0:
            self.q_load.setValue(self.bus.q_load)
        else:
            self.q_load.clearValue()
        if self.bus.p_gen != 0:
            self.p_gen.setValue(self.bus.p_gen)
        else:
            self.p_gen.clearValue()
        if self.bus.q_gen != 0:
            self.q_gen.setValue(self.bus.q_gen)
        else:
            self.q_gen.clearValue()
        if self.bus.q_min != float("-inf"):
            self.q_min.setValue(self.bus.q_min)
        else:
            self.q_min.clearValue()
        if self.bus.q_max != float("inf"):
            self.q_max.setValue(self.bus.q_max)
        else:
            self.q_max.clearValue()
        if self.bus.g_shunt != 0:
            self.shunt_g.setValue(self.bus.g_shunt)
        else:
            self.shunt_g.clearValue()
        if self.bus.b_shunt != 0:
            self.shunt_b.setValue(self.bus.b_shunt)
        else:
            self.shunt_b.clearValue()

    def circuit_listener(self, element: NetworkElement, event: ElementEvent):
        if event is ElementEvent.UPDATED and isinstance(element, Bus) and element.id == self.bus.id:
            self.bus = element
            self.update_values()
            return
