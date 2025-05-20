from PySide6.QtWidgets import QHBoxLayout, QComboBox

from controllers.simulator_controller import SimulatorController

from models.bus import Bus
from models.network_element import ElementEvent
from view.circuit_tiles.components.element_tile import ElementTile
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
        self.busTypeDropdown.addItems(["Slack", "PV", "PQ"])
        layout.addWidget(self.busTypeDropdown)

        # "v"
        self.voltageField = TextField[float](
            type=float,
            validators=[NotEmptyValidator(), NumberValidator(min=0)],
        )
        layout.addWidget(self.voltageField)

        # "o" (angle)
        self.angleField = TextField[float](
            type=float,
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
        if self.element.load:
            self.p_load.setValue(self.element.load.real)
            self.q_load.setValue(self.element.load.imag)
        if self.element.generator:
            self.p_gen.setValue(self.element.generator.real)
            self.q_gen.setValue(self.element.generator.imag)
        if self.element.q_min is not None:
            self.q_min.setValue(self.element.q_min)
        if self.element.q_max is not None:
            self.q_max.setValue(self.element.q_max)
        self.shunt_b.setValue(self.element.shunt.real)
        self.shunt_g.setValue(self.element.shunt.imag)
        return

    def edit(self):
        # Validate every field: nameField, numberField, voltageField, etc.
        for validator in [
            self.nameField.validate,
            self.numberField.validate,
            self.voltageField.validate,
            self.angleField.validate,
            self.p_load.validate,
            self.q_load.validate,
            self.p_gen.validate,
            self.q_gen.validate,
            self.q_min.validate,
            self.q_max.validate,
            self.shunt_b.validate,
            self.shunt_g.validate,
        ]:
            if not validator():
                return

        # Gather corrected values.
        # Create a copy/update of your element using values from the fields.
        copy = self.element.copyWith(
            name=self.nameField.getValue(),
            number=self.numberField.getValue(),
            type=self.busTypeDropdown.currentText(),
            v=self.voltageField.getValue(),
            o=self.angleField.getValue(),
            p_load=self.p_load.getValue(),
            q_load=self.q_load.getValue(),
            p_gen=self.p_gen.getValue(),
            q_gen=self.q_gen.getValue(),
            q_min=self.q_min.getValue(),
            q_max=self.q_max.getValue(),
            shunt_b=self.shunt_b.getValue(),
            shunt_g=self.shunt_g.getValue(),
        )

        SimulatorController.instance().updateElement(copy)

    def circuitListener(self, element: Bus, event: ElementEvent):
        super().circuitListener(element, event)

        # TODO: handle updates if needed.
        # if event == ElementEvent.UPDATED and element.id in self.element.connection_ids:
        #     self.update_form_values()
