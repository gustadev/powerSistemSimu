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
        self.__buses = dict[str, Bus]()
        self.__connections = dict[str, BusConnection]()
        self.__listeners: list[Callable[[NetworkElement, ElementEvent], None]] = []

    def listen(self, callback: Callable[[NetworkElement, ElementEvent], None]) -> None:
        self.__listeners.append(callback)

    def addBus(self, bus: Bus = Bus()) -> Bus:
        return cast(Bus, self.__add_element(bus))

    def addConnection(self, line: BusConnection) -> BusConnection:
        return cast(BusConnection, self.__add_element(line))

    def __add_element(self, element: NetworkElement) -> NetworkElement:
        if isinstance(element, Bus):
            self.__buses[element.id] = element
        elif isinstance(element, BusConnection):
            self.__connections[element.id] = element

        for callback in self.__listeners:
            callback(element, ElementEvent.CREATED)

        return element

    def updateElement(self, element: NetworkElement) -> None:
        if element.id in self.__buses and isinstance(element, Bus):
            self.__buses[element.id] = element
        elif element.id in self.__connections and isinstance(element, BusConnection):
            self.__connections[element.id] = element
        else:
            return

        for callback in self.__listeners:
            callback(element, ElementEvent.UPDATED)

    def get_bus_by_id(self, id: str) -> Bus:
        if id in self.__buses:
            return self.__buses[id]
        raise ValueError(f"Bus with id {id} not found")

    def get_connection_by_id(self, id: str) -> BusConnection:
        if id in self.__connections:
            return self.__connections[id]
        raise ValueError(f"Connection with id {id} not found")

    def runPowerFlow(self):
        power_flow = PowerFlow()
        for bus in self.__buses.values():
            power_flow.add_bus(bus)
        for connection in self.__connections.values():
            power_flow.add_connection(connection)
        power_flow.solve()

        for bus in self.__buses.values():
            for callback in self.__listeners:
                callback(bus, ElementEvent.UPDATED)
        

    def printNetwork(self):
        print("Network:")
        print("Buses:")
        for bus in self.__buses:
            print(bus)
        print("Connections:")
        for connection in self.__connections:
            print(connection)

    def getElementNames(self, ids: list[str]) -> str:
        return " "  # TODO
