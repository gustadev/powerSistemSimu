from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
)

from controllers.simulator_controller import ElementEvent, SimulatorController
from models.bus import Bus
from models.network_element import NetworkElement
from view.bus_table_row import BusTableRow


class BusTable(QWidget):
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

        self.items: list[str] = []
        for bus in self.simulatorInstance.buses:
            row = self.table.rowCount()
            self.table.insertRow(row)
            bus_row = BusTableRow(bus)
            widgets = bus_row.get_widgets()
            for col, widget in enumerate(widgets):
                self.table.setCellWidget(row, col, widget)
            self.items.append(bus.id)

    def circuitListener(self, element: NetworkElement, event: ElementEvent):
        if event is ElementEvent.CREATED and isinstance(element, Bus):
            row = self.table.rowCount()
            self.table.insertRow(row)
            bus_row = BusTableRow(element)
            widgets = bus_row.get_widgets()
            for col, widget in enumerate(widgets):
                self.table.setCellWidget(row, col, widget)
            self.items.append(element.id)

        if event is ElementEvent.DELETED and isinstance(element, Bus):
            for i, bus_id in enumerate(self.items):
                if bus_id == element.id:
                    self.table.removeRow(i)
                    self.items.pop(i)
                    break
