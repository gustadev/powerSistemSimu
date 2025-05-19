from typing import Callable

from maths.power_flow import PowerFlow
from models.bus import Bus
from models.connection import BusConnection
from models.network_element import ElementEvent, NetworkElement


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

    def addBus(self) -> None:
        self.__add_element(Bus())

    def addConnection(self, source: Bus, target: Bus) -> None:
        line = BusConnection(source, target, y=complex(1))
        self.__add_element(line)

    def __add_element(self, element: NetworkElement) -> None:
        if isinstance(element, Bus):
            element = self.__network.add_bus(element)
        elif isinstance(element, BusConnection):
            self.__network.add_connection(element)

        for callback in self.__listeners:
            callback(element, ElementEvent.CREATED)

    def updateElement(self, element: NetworkElement) -> None:
        if isinstance(element, Bus):
            for index, bus in enumerate(self.__network.buses):
                if bus.number == element.number:
                    self.__network.buses[index] = element
                    break
        elif isinstance(element, BusConnection):
            for index, connection in enumerate(self.__network.connections):
                if connection.number == element.number:
                    self.__network.connections[index] = element
                    break

        for callback in self.__listeners:
            callback(element, ElementEvent.UPDATED)

    def getElementByNumber(self, number: str) -> NetworkElement | None:
        if isinstance(number, Bus):
            for bus in self.__network.buses:
                if bus.number == number:
                    return bus
        elif isinstance(number, BusConnection):
            for connection in self.__network.connections:
                if connection.number == number:
                    return connection
        return None

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
