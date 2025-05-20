from typing import Callable

from maths.power_flow import PowerFlow
from models.bus import Bus
from models.connection import BusConnection
from models.network_element import ElementEvent, NetworkElement
from typing import cast


class SimulatorController:
    __instance = None

    @staticmethod
    def instance():
        if SimulatorController.__instance is None:
            SimulatorController.__instance = SimulatorController()
        return SimulatorController.__instance

    def __init__(self):
        self.__network = PowerFlow()  # TODO rename to network
        self.__listeners: list[Callable[[NetworkElement, ElementEvent], None]] = []

    def listen(self, callback: Callable[[NetworkElement, ElementEvent], None]) -> None:
        self.__listeners.append(callback)

    def addBus(self) -> Bus:
        return cast(Bus, self.__add_element(Bus()))

    def addConnection(self, source: Bus, target: Bus) -> BusConnection:
        line = BusConnection(source, target, y=complex(1))
        return cast(BusConnection, self.__add_element(line))

    def __add_element(self, element: NetworkElement) -> NetworkElement:
        if isinstance(element, Bus):
            element = self.__network.add_bus(element)
        elif isinstance(element, BusConnection):
            self.__network.add_connection(element)

        for callback in self.__listeners:
            callback(element, ElementEvent.CREATED)

        return element

    def updateElement(self, element: NetworkElement) -> None:
        if element.id in self.__network.buses and isinstance(element, Bus):
            self.__network.buses[element.id] = element
        elif id in self.__network.connections and isinstance(element, BusConnection):
            self.__network.connections[element.id] = element
        else:
            return

        for callback in self.__listeners:
            callback(element, ElementEvent.UPDATED)

    def get_bus_by_id(self, id: int) -> Bus:
        if id in self.__network.buses:
            return self.__network.buses[id]
        raise ValueError(f"Bus with id {id} not found")

    def get_connection_by_id(self, id: int) -> BusConnection:
        if id in self.__network.connections:
            return self.__network.connections[id]
        raise ValueError(f"Connection with id {id} not found")

    def runPowerFlow(self):
        self.__network.solve()

    def printNetwork(self):
        print("Network:")
        print("Buses:")
        for bus in self.__network.buses:
            print(bus)
        print("Connections:")
        for connection in self.__network.connections:
            print(connection)

    def getElementNames(self, ids: list[str]) -> str:
        return " "  # TODO
