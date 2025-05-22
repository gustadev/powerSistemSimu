from typing import Tuple
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QComboBox,
)

from controllers.simulator_controller import ElementEvent, SimulatorController
from models.bus import Bus, BusType
from models.network_element import NetworkElement
from view.circuit_tiles.components.text_field import TextField


# A new helper class representing a Bus row in the table.
class BusTableRow:
    def __init__(self, bus: Bus):
        SimulatorController.instance().listen(self.circuit_listener)
        self.bus = bus

        # "name"
        self.nameField = TextField(type=str)
        self.nameField.setValue(self.bus.name)

        # "number"
        self.numberField = TextField[int](type=int, on_focus_out=self.save)
        self.numberField.setValue(self.bus.number)

        # "type" - using dropdown
        self.busTypeDropdown = QComboBox()
        self.busTypeDropdown.addItems(["SLACK", "PV", "PQ"])
        index = self.busTypeDropdown.findText(self.bus.type.name)
        if index >= 0:
            self.busTypeDropdown.setCurrentIndex(index)
        self.busTypeDropdown.currentIndexChanged.connect(self.save)

        # "v"
        self.voltageField = TextField[float](type=float, on_focus_out=self.save)
        self.voltageField.setValue(self.bus.v)

        # "o" (angle)
        self.angleField = TextField[float](type=float, on_focus_out=self.save)
        self.angleField.setValue(self.bus.o)

        # "p" (read-only field)
        self.p_field = TextField[float](type=float, enabled=False)
        self.p_field.setValue(self.bus.p)

        # "q" (read-only field)
        self.q_field = TextField[float](type=float, enabled=False)
        self.q_field.setValue(self.bus.q)

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
        SimulatorController.instance().updateElement(
            self.bus.copy_with(
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

    def update_values(self) -> None:
        self.nameField.setValue(self.bus.name)
        self.numberField.setValue(self.bus.number)
        idx = self.busTypeDropdown.findText(self.bus.type.name)
        if idx >= 0:
            self.busTypeDropdown.setCurrentIndex(idx)
        self.voltageField.setValue(self.bus.v)
        self.angleField.setValue(self.bus.o)
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
        if event is ElementEvent.UPDATED:
            if isinstance(element, Bus) and element.id == self.bus.id:
                self.bus = element
                self.update_values()


# Updated BusList that uses a table.
class BusList(QWidget):
    def __init__(self):
        super().__init__()
        self.simulatorInstance = SimulatorController.instance()
        self.simulatorInstance.listen(self.circuitListener)
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.fields = [
            "name",
            "number",
            "type",
            "v",
            "o",
            "p",
            "q",
            "p_load",
            "q_load",
            "p_gen",
            "q_gen",
            "q_min",
            "q_max",
            "shunt_b",
            "shunt_g",
        ]
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.fields))
        self.table.setHorizontalHeaderLabels(self.fields)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        # Dictionary key: bus.id -> (BusTableRow instance, row index)
        self.items: dict[int, Tuple[BusTableRow, int]] = {}

    def circuitListener(self, element: NetworkElement, event: ElementEvent):
        if event is ElementEvent.CREATED:
            if isinstance(element, Bus):
                row = self.table.rowCount()
                self.table.insertRow(row)
                bus_row = BusTableRow(element)
                widgets = bus_row.get_widgets()
                for col, widget in enumerate(widgets):
                    self.table.setCellWidget(row, col, widget)
                self.items[element.id] = (bus_row, row)
