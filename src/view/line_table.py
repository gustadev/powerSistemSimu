from typing import Tuple
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
)

from controllers.simulator_controller import ElementEvent, SimulatorController
from models.connection import BusConnection
from models.network_element import NetworkElement
from view.line_table_row import LineTableRow


class LineTable(QWidget):
    def __init__(self):
        super().__init__()
        self.simulatorInstance = SimulatorController.instance()
        self.simulatorInstance.listen(self.circuitListener)
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.fields = [
            "tap bus",
            "z bus",
            "",
            "r",
            "x",
            "g",
            "b",
            "bc",
            "tap",
        ]

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.fields))
        self.table.setHorizontalHeaderLabels(self.fields)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        self.items: dict[str, Tuple[LineTableRow, int]] = {}
        for line in self.simulatorInstance.connections:
            row = self.table.rowCount()
            self.table.insertRow(row)
            line_row = LineTableRow(line)
            widgets = line_row.get_widgets()
            for col, widget in enumerate(widgets):
                self.table.setCellWidget(row, col, widget)
            self.items[line.id] = (line_row, row)

    def circuitListener(self, element: NetworkElement, event: ElementEvent):
        if event is ElementEvent.CREATED:
            if isinstance(element, BusConnection):
                row = self.table.rowCount()
                self.table.insertRow(row)
                bus_row = LineTableRow(element)
                widgets = bus_row.get_widgets()
                for col, widget in enumerate(widgets):
                    self.table.setCellWidget(row, col, widget)
                self.items[element.id] = (bus_row, row)
