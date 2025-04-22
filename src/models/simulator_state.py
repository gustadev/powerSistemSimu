from typing import *
import numpy as np
import pypsa

from models.circuit_node import (
    BusNode,
    CircuitNode,
    GeneratorNode,
    LoadNode,
    TransmissionLineNode,
)


class SimulatorState:
    __instance = None

    @staticmethod
    def instance():
        if SimulatorState.__instance is None:
            SimulatorState.__instance = SimulatorState()
        return SimulatorState.__instance

    def __init__(self):
        self.elements = dict()
        self.network = pypsa.Network()
        self.onWireCreated: Callable[
            [CircuitNode, CircuitNode, TransmissionLineNode], None
        ]
        self.onNodeCreated: Callable[[CircuitNode], None] = None

    def addBus(self) -> None:
        bus = BusNode(v_nom=1)
        self.setElement(bus)
        self.onNodeCreated(bus)

    def addGenerator(self) -> None:
        generator = GeneratorNode(p_set=1, control="GM")
        self.setElement(generator)
        self.onNodeCreated(generator)

    def addLoad(self) -> None:
        load = LoadNode(p_set=1)
        self.setElement(load)
        self.onNodeCreated(load)

    def setElement(self, node: CircuitNode) -> None:
        self.elements.setdefault(node.id, node)
        if isinstance(node, BusNode):
            self.network.add(
                node.type,
                node.id,
                v_nom=node.v_nom,
                overwrite=True,
            )
        elif isinstance(node, GeneratorNode):
            self.network.add(
                node.type,
                node.id,
                p_set=node.p_set,
                control=node.control,
                bus=node.busId,
                overwrite=True,
            )
        elif isinstance(node, LoadNode):
            self.network.add(
                node.type,
                node.id,
                p_set=node.p_set,
                bus=node.busId,
                overwrite=True,
            )
        elif isinstance(node, TransmissionLineNode):
            self.network.add(
                node.type,
                node.id,
                bus0=node.sourceId,
                bus1=node.targetId,
                x=node.x,
                r=node.r,
                overwrite=True,
            )
        else:
            raise ValueError(f"Unknown node type: {node.type}")

    def addConnection(self, sourceNode: CircuitNode, targetNode: CircuitNode) -> None:
        if not isinstance(sourceNode, BusNode) and not isinstance(targetNode, BusNode):
            print("Cannot connect non-bus elements")
            return

        busNode: BusNode = None
        otherNode: CircuitNode = None
        if isinstance(sourceNode, BusNode):
            busNode = sourceNode
            otherNode = targetNode
        else:
            busNode = targetNode
            otherNode = sourceNode

        if isinstance(otherNode, BusNode):
            if otherNode.id in busNode.connectionIds:
                print(
                    f"Connection already exists between {busNode.id} and {otherNode.id}"
                )
                return

            busNode.connectionIds.append(otherNode.id)
            otherNode.connectionIds.append(busNode.id)
            line = TransmissionLineNode(0.1, 0.01, busNode.id, otherNode.id)
            self.setElement(line)

            print(f"{line} created between {busNode.id} and {otherNode.id}")
            self.onWireCreated(busNode, otherNode, line)
            return

        if isinstance(otherNode, GeneratorNode):
            if otherNode.busId:
                print(f"{otherNode.id} already connected")
                return

            busNode.connectionIds.append(otherNode.id)
            otherNode.busId = busNode.id
            self.setElement(otherNode)
            print(f"{otherNode} connected to {busNode.id}")
            self.onWireCreated(busNode, otherNode, None)
            return

        if isinstance(otherNode, LoadNode):
            if otherNode.busId:
                print(f"{otherNode.id} already connected")
                return

            busNode.connectionIds.append(otherNode.id)
            otherNode.busId = busNode.id
            self.setElement(otherNode)
            print(f"{otherNode} connected to {busNode.id}")
            self.onWireCreated(busNode, otherNode, None)
            return
        return

    def runPowerFlow(self):
        try:
            self.network.pf()
            print("Power flow results:")
            print(self.network.lines_t.p0)
            print(self.network.buses_t.v_ang * 180 / np.pi)
            print(self.network.buses_t.v_mag_pu)
        except Exception as e:
            print(f"Power flow failed: {e}")
