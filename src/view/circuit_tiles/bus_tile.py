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
            on_focus_out=self.save,
        )
        layout.addWidget(self.numberField)

        # "type" - using a dropdown for bus type.
        self.busTypeDropdown = QComboBox()
        # order: "Slack", "PV", "PQ" (adjust if needed)
        self.busTypeDropdown.addItems(["SLACK", "PV", "PQ"])
        self.busTypeDropdown.currentIndexChanged.connect(self.save)
        layout.addWidget(self.busTypeDropdown)

        # "v"
        self.voltageField = TextField[float](
            type=float,
            default_Value=1.0,
            validators=[NotEmptyValidator(), NumberValidator(min=0)],
            on_focus_out=self.save,
        )
        layout.addWidget(self.voltageField)

        # "o" (angle)
        self.angleField = TextField[float](
            type=float,
            default_Value=0.0,
            validators=[NotEmptyValidator(), NumberValidator()],
            on_focus_out=self.save,
        )
        layout.addWidget(self.angleField)

        # "p_load"
        self.p_load = TextField[float](
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
            on_focus_out=self.save,
        )
        layout.addWidget(self.p_load)

        # "q_load"
        self.q_load = TextField[float](
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
            on_focus_out=self.save,
        )
        layout.addWidget(self.q_load)

        # "p_gen"
        self.p_gen = TextField[float](
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
            on_focus_out=self.save,
        )
        layout.addWidget(self.p_gen)

        # "q_gen"
        self.q_gen = TextField[float](
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
            on_focus_out=self.save,
        )
        layout.addWidget(self.q_gen)

        # "q_min" (was previously min_q)
        self.q_min = TextField[float](
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
            on_focus_out=self.save,
        )
        layout.addWidget(self.q_min)

        # "q_max" (was previously max_q)
        self.q_max = TextField[float](
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
            on_focus_out=self.save,
        )
        layout.addWidget(self.q_max)

        # "shunt_b"
        self.shunt_b = TextField[float](
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
            on_focus_out=self.save,
        )
        layout.addWidget(self.shunt_b)

        # "shunt_g"
        self.shunt_g = TextField[float](
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
            on_focus_out=self.save,
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
        if self.element.p_load != 0:
            self.p_load.setValue(self.element.p_load)
        else:
            self.p_load.clearValue()
        if self.element.q_load != 0:
            self.q_load.setValue(self.element.q_load)
        else:
            self.q_load.clearValue()
        if self.element.p_gen != 0:
            self.p_gen.setValue(self.element.p_gen)
        else:
            self.p_gen.clearValue()
        if self.element.q_gen != 0:
            self.q_gen.setValue(self.element.q_gen)
        else:
            self.q_gen.clearValue()
        if self.element.q_min != float("-inf"):
            self.q_min.setValue(self.element.q_min)
        else:
            self.q_min.clearValue()
        if self.element.q_max != float("inf"):
            self.q_max.setValue(self.element.q_max)
        else:
            self.q_max.clearValue()
        if self.element.g_shunt != 0:
            self.shunt_g.setValue(self.element.g_shunt)
        else:
            self.shunt_g.clearValue()
        if self.element.b_shunt != 0:
            self.shunt_b.setValue(self.element.b_shunt)
        else:
            self.shunt_b.clearValue()

        return

    def validate(self) -> bool:
        return True  # TODO implement validation

    def save(self) -> None:
        bus_type: BusType = BusType[self.busTypeDropdown.currentText()]

        SimulatorController.instance().updateElement(
            self.element.copy_with(
                name=self.nameField.getValue(),
                number=self.numberField.getValue(),
                type=bus_type,
                v=self.voltageField.getValue(),
                o=self.angleField.getValue(),
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

    def circuitListener(self, element: NetworkElement, event: ElementEvent):
        super().circuitListener(element, event)
