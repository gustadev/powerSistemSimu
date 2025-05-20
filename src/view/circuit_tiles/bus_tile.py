from PySide6.QtWidgets import QHBoxLayout, QComboBox

from controllers.simulator_controller import SimulatorController

from models.bus import Bus
from models.network_element import ElementEvent, NetworkElement
from view.circuit_tiles.components.element_tile import ElementTile
from models.bus import BusType
from view.circuit_tiles.components.text_field import (
    NotEmptyValidator,
    NumberValidator,
    TextField,
)


class BusTile(ElementTile[Bus]):
    def __init__(self, element: Bus):
        super().__init__(element=element, type=Bus)

    def build_form(self, layout: QHBoxLayout):
        self.nameField = TextField(type=str, validators=[NotEmptyValidator()])
        layout.addWidget(self.nameField)

        # "number"
        self.numberField = TextField[int](
            type=int,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.numberField)

        # "type" - using a dropdown for bus type.
        self.busTypeDropdown = QComboBox()
        # order: "Slack", "PV", "PQ" (adjust if needed)
        self.busTypeDropdown.addItems(["SLACK", "PV", "PQ"])
        layout.addWidget(self.busTypeDropdown)

        # "v"
        self.voltageField = TextField[float](
            type=float,
            default_Value=1.0,
            validators=[NotEmptyValidator(), NumberValidator(min=0)],
        )
        layout.addWidget(self.voltageField)

        # "o" (angle)
        self.angleField = TextField[float](
            type=float,
            default_Value=0.0,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.angleField)

        # "p_load"
        self.p_load = TextField[float](
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.p_load)

        # "q_load"
        self.q_load = TextField[float](
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.q_load)

        # "p_gen"
        self.p_gen = TextField[float](
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.p_gen)

        # "q_gen"
        self.q_gen = TextField[float](
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.q_gen)

        # "q_min" (was previously min_q)
        self.q_min = TextField[float](
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.q_min)

        # "q_max" (was previously max_q)
        self.q_max = TextField[float](
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.q_max)

        # "shunt_b"
        self.shunt_b = TextField[float](
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.shunt_b)

        # "shunt_g"
        self.shunt_g = TextField[float](
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.shunt_g)

    def update_form_values(self):
        super().update_form_values()
        self.nameField.setValue(self.element.name)
        self.numberField.setValue(self.element.number)
        index = self.busTypeDropdown.findText(self.element.type.name)
        if index >= 0:
            self.busTypeDropdown.setCurrentIndex(index)
        self.voltageField.setValue(self.element.v)
        self.angleField.setValue(self.element.o)
        if self.element.load and self.element.load.real != 0.0:
            self.p_load.setValue(self.element.load.real)
        else:
            self.p_load.clearValue()
        if self.element.load and self.element.load.imag != 0.0:
            self.q_load.setValue(self.element.load.imag)
        else:
            self.p_load.clearValue()
        if self.element.generator and self.element.generator.real != 0.0:
            self.p_gen.setValue(self.element.generator.real)
        if self.element.generator and self.element.generator.imag != 0.0:
            self.q_gen.setValue(self.element.generator.imag)
        if self.element.q_min is not None and self.element.q_min != 0.0:
            self.q_min.setValue(self.element.q_min)
        if self.element.q_max is not None and self.element.q_max != 0.0:
            self.q_max.setValue(self.element.q_max)
        if self.element.shunt.real != 0.0:
            self.shunt_b.setValue(self.element.shunt.real)
        if self.element.shunt.imag != 0.0:
            self.shunt_g.setValue(self.element.shunt.imag)
        return

    def validate(self) -> bool:
        return True  # TODO implement validation

    def save(self) -> None:
        name = self.nameField.getValue()
        number = self.numberField.getValue()
        bus_type = self.busTypeDropdown.currentText()
        voltage = self.voltageField.getValue()
        angle = self.angleField.getValue()
        p_load = self.p_load.getValue()
        q_load = self.q_load.getValue()
        p_gen = self.p_gen.getValue()
        q_gen = self.q_gen.getValue()
        q_min = self.q_min.getValue()
        q_max = self.q_max.getValue()
        shunt_b = self.shunt_b.getValue()
        shunt_g = self.shunt_g.getValue()
        if name is None:
            name = self.element.name
        if number is None:
            number = self.element.number
        self.element.type = BusType[bus_type]
        SimulatorController.instance().updateElement(
            self.element.copy_with(
                name=name,
                number=number,
                v=voltage,
                o=angle,
                load=complex(p_load if p_load else 0.0, q_load if q_load else 0.0),
                generator=complex(p_gen if p_gen else 0.0, q_gen if q_gen else 0.0),
                q_min=q_min if q_min else 0.0,
                q_max=q_max if q_max else 0.0,
                shunt=complex(shunt_b if shunt_b else 0.0, shunt_g if shunt_g else 0.0),
                type=self.element.type,
            ),
        )

    def circuitListener(self, element: NetworkElement, event: ElementEvent):
        super().circuitListener(element, event)
