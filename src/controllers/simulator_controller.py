from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy

from typing import Callable

from maths.power_flow import PowerFlow
from models.bus import Bus
from models.line import Line
from models.network_element import ElementEvent, NetworkElement
from typing import cast
from view.results_view import ResultsView



class SimulatorController:
    __instance = None

    @staticmethod
    def instance():
        if SimulatorController.__instance is None:
            SimulatorController.__instance = SimulatorController()
        return SimulatorController.__instance

    def clear_state(self):
        for bus in self.__buses.values():
            for listener in self.__listeners:
                listener(bus, ElementEvent.DELETED)
        for connection in self.__connections.values():
            for listener in self.__listeners:
                listener(connection, ElementEvent.DELETED)
        self.__buses.clear()
        self.__connections.clear()

    @property
    def buses(self) -> list[Bus]:
        return list(self.__buses.values())

    @property
    def connections(self) -> list[Line]:
        return list(self.__connections.values())

    def __init__(self):
        self.__buses = dict[str, Bus]()
        self.__connections = dict[str, Line]()
        self.__listeners: list[Callable[[NetworkElement, ElementEvent], None]] = []
        self.power_base_mva: float = 100.0
        self.__results = ResultsView()

    def listen(self, callback: Callable[[NetworkElement, ElementEvent], None]) -> None:
        self.__listeners.append(callback)

    def addBus(self, bus: Bus | None = None) -> Bus:
        return cast(Bus, self.__add_element(bus if bus else Bus()))

    def addConnection(self, line: Line) -> Line:
        return cast(Line, self.__add_element(line))

    def __add_element(self, element: NetworkElement) -> NetworkElement:
        if isinstance(element, Bus):
            self.__buses[element.id] = element
        elif isinstance(element, Line):
            self.__connections[element.id] = element

        for callback in self.__listeners:
            callback(element, ElementEvent.CREATED)

        return element

    def updateElement(self, element: NetworkElement) -> None:
        if element.id in self.__buses and isinstance(element, Bus):
            self.__buses[element.id] = element
        elif element.id in self.__connections and isinstance(element, Line):
            self.__connections[element.id] = element
        else:
            return

        for callback in self.__listeners:
            callback(element, ElementEvent.UPDATED)

    def get_bus_by_id(self, id: str) -> Bus:
        if id in self.__buses:
            return self.__buses[id]
        raise ValueError(f"Bus with id {id} not found")

    def get_connection_by_id(self, id: str) -> Line:
        if id in self.__connections:
            return self.__connections[id]
        raise ValueError(f"Connection with id {id} not found")
    def get_results(self) -> str:
        return self.__results
    def clear_results(self):
        self.__results = ""
    def runPowerFlow(self):
        power_flow = PowerFlow(base=self.power_base_mva)
        for bus in self.__buses.values():
            power_flow.add_bus(bus)
        for connection in self.__connections.values():
            power_flow.add_connection(connection)
        power_flow.solve()

        for bus in self.__buses.values():
            for callback in self.__listeners:
                callback(bus, ElementEvent.UPDATED)

    def printNetwork(self):
        pf = PowerFlow()
        for bus in self.__buses.values():
            bus = bus.copy_with()
            pf.add_bus(bus)
        for line in self.__connections.values():
            line = line.copyWith()
            pf.add_connection(line)
        pf.print_data()

    def getElementNames(self, ids: list[str]) -> str:
        return " "  # TODO

    def showResults(self):
        resultsWindow = QMainWindow()
        resultsWindow.setWindowTitle("Results")
        centralWidget = QWidget()
        layout = QVBoxLayout(centralWidget)
        layout.setContentsMargins(0, 0, 0, 0)

        rightWidget = self.__results
        rightWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        layout.addWidget(rightWidget)

        resultsWindow.setCentralWidget(centralWidget)
        resultsWindow.resize(800, 600)
        resultsWindow.show()
        self.__resultsWindow = resultsWindow
        