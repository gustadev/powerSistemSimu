from PySide6.QtWidgets import QVBoxLayout

from controllers.simulator_controller import SimulatorController

from models.bus import Bus
from models.network_element import ElementEvent
from view.circuit_tiles.components.element_tile import ElementTile
from PySide6.QtWidgets import QComboBox
from view.circuit_tiles.components.text_field import (
    NotEmptyValidator,
    NumberValidator,
    TextField,
)


class BusTile(ElementTile[Bus]):
    def __init__(self, element: Bus):
        super().__init__(element=element, type=Bus)

    def build_form(self, layout: QVBoxLayout):
        super().build_form(layout)
        self.voltageField = TextField[float](
            title="v",
            trailing="pu",
            type=float,
            validators=[NotEmptyValidator(), NumberValidator(min=0)],
        )
        layout.addWidget(self.voltageField)

        self.angleField = TextField[float](
            title="o",
            trailing="deg",
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.angleField)
        self.p_gen = TextField[float](
            title="P_gen",
            trailing="pu",
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.p_gen)

        self.q_gen = TextField[float](
            title="Q_gen",
            trailing="pu",
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.q_gen)

        self.p_load = TextField[float](
            title="P_load",
            trailing="pu",
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.p_load)
        self.q_load = TextField[float](
            title="Q_load",
            trailing="pu",
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.q_load)

        self.max_q = TextField[float](
            title="Q_max",
            trailing="pu",
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.max_q)

        self.min_q = TextField[float](
            title="Q_min",
            trailing="pu",
            type=float,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.min_q)

        self.shuntField = TextField[complex](
            title="shunt",
            trailing="pu",
            type=complex,
            validators=[NotEmptyValidator(), NumberValidator()],
        )
        layout.addWidget(self.shuntField)
        self.busTypeDropdown = QComboBox()
        self.busTypeDropdown.addItems(["Slack", "PV", "PQ"])
        layout.addWidget(self.busTypeDropdown)

    def update_form_values(self):
        super().update_form_values()
        self.voltageField.setValue(self.element.v)
        # self.connectionsField.setValue(
        #     SimulatorController.instance().getElementNames(self.element.connection_ids)
        # )
        return

    def edit(self):
        for validator in [self.nameField.validate, self.voltageField.validate]:
            if not validator():
                return

        # copy = self.element.copyWith(
        #     name=self.nameField.getValue(), v_nom=self.voltageField.getValue()
        # )

        SimulatorController.instance().updateElement(copy)

    def circuitListener(self, element: Bus, event: ElementEvent):
        super().circuitListener(element, event)

        # TODO
        # if event == ElementEvent.UPDATED and element.id in self.element.connection_ids:
        #     self.update_form_values()
