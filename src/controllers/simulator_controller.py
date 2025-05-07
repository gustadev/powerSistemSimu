from typing import *
import numpy as np
import pypsa

from enums.element_event import ElementEvent
from models.bus import BusNode
from models.circuit_element import CircuitElement, DoubleConnectionElement
from models.generator import GeneratorNode
from models.load import LoadNode
from models.transmission_line import TransmissionLineElement
from models.wire import WireElement


class SimulatorController:
    __instance = None

    @staticmethod
    def instance():
        if SimulatorController.__instance is None:
            SimulatorController.__instance = SimulatorController()
        return SimulatorController.__instance

    def __init__(self):
        self.__elements = dict()
        self.__network = pypsa.Network()
        self.__listeners: list[Callable[[CircuitElement, ElementEvent], None]] = []

    def listen(self, callback: Callable[[CircuitElement, ElementEvent], None]) -> None:
        self.__listeners.append(callback)

    def __updateElement(self, node: CircuitElement, event: ElementEvent | None) -> None:
        self.__elements[node.id] = node
        if isinstance(node, BusNode):
            self.__network.add(
                node.type,
                node.id,
                v_nom=node.v_nom,
                overwrite=True,
            )
        elif isinstance(node, GeneratorNode):
            self.__network.add(
                node.type,
                node.id,
                p_nom=node.nominal_power,
                control=node.control,
                bus=node.connection_id,
                overwrite=True,
            )
        elif isinstance(node, LoadNode):
            self.__network.add(
                node.type,
                node.id,
                p_set=node.p_set,
                bus=node.connection_id,
                overwrite=True,
            )
        elif isinstance(node, TransmissionLineElement):
            self.__network.add(
                node.type,
                node.id,
                bus0=node.source_id,
                bus1=node.target_id,
                x=node.reactance,
                r=node.resistance,
                b=node.susceptance,
                g=node.conductance,
                overwrite=True,
            )
        if event:
            for callback in self.__listeners:
                callback(node, event)

    def addBus(self) -> None:
        # bus = BusNode()
        self.__updateElement(BusNode(), event=ElementEvent.CREATED)

    def addGenerator(self) -> None:
        # generator = GeneratorNode()
        self.__updateElement(GeneratorNode(), ElementEvent.CREATED)

    def addLoad(self) -> None:
        # load = LoadNode()
        self.__updateElement(LoadNode(), ElementEvent.CREATED)

    # TODO update everyone on links
    def addConnection(self, sourceNode: CircuitElement, targetNode: CircuitElement) -> None:
        if not isinstance(sourceNode, BusNode) and not isinstance(targetNode, BusNode):
            print("Cannot connect non-bus elements")
            return

        busNode: BusNode = None
        otherNode: CircuitElement = None
        connectionElement: DoubleConnectionElement = None

        (busNode, otherNode) = (sourceNode, targetNode) if isinstance(sourceNode, BusNode) else (targetNode, sourceNode)

        if isinstance(otherNode, BusNode):
            for elementId in list(busNode.connection_ids):
                element = self.getElementById(elementId)
                if isinstance(
                    element, TransmissionLineElement
                ) and element.isConnectedTo(otherNode.id):
                    print(
                        f"Connection already exists between {busNode.name} and {otherNode.name} through {element.name}"
                    )
                    return

            connectionElement = TransmissionLineElement(
                source_id=busNode.id, target_id=otherNode.id
            )
            busNode = busNode.copyWith(
                connection_ids=busNode.connection_ids + (connectionElement.id,)
            )
            otherNode = otherNode.copyWith(
                connection_ids=otherNode.connection_ids + (connectionElement.id,)
            )

        if isinstance(otherNode, LoadNode) or isinstance(otherNode, GeneratorNode):
            if otherNode.connection_id:
                print(f"{otherNode.name} already connected")
                return

            busNode = busNode.copyWith(
                connection_ids=busNode.connection_ids + (otherNode.id,)
            )
            otherNode = otherNode.copyWith(connection_id=busNode.id)
            connectionElement = WireElement(busNode.id, otherNode.id)

        if connectionElement:
            self.__updateElement(connectionElement, ElementEvent.CREATED)
            self.__updateElement(busNode, ElementEvent.UPDATED)
            self.__updateElement(otherNode, ElementEvent.UPDATED)

    def updateElement(self, node: CircuitElement) -> None:
        if node.id not in self.__elements:
            print(f"Element {node.name} not found")
            return

        self.__updateElement(node, ElementEvent.UPDATED)

    def getElementById(self, id: str) -> CircuitElement | None:
        if id in self.__elements:
            return self.__elements[id]
        return None

    def runPowerFlow(self):
        try:
            self.__network.pf()
            print("Power flow results:")
            print(self.__network.lines_t.p0)
            print(self.__network.buses_t.v_ang * 180 / np.pi)
            print(self.__network.buses_t.v_mag_pu)

        except Exception as e:
            print(f"Power flow failed: {e}")

    def printNetwork(self):
        print("Network:")
        print(self.__network.lines)
        print(self.__network.buses)
        print(self.__network.generators)
        print(self.__network.loads)
        print(self.__network.links)
        self.__network.export_to_csv_folder("Output_Data")
        

    def getElementNames(self, ids: list[str]) -> str:
        names = []
        for id in ids:
            if id in self.__elements:
                names.append(self.getElementById(id).name)

        return ", ".join(names)
