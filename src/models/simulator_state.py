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
    def __init__(self):
        self.elements = dict()
        self.network = pypsa.Network()

    def setNode(self, node: CircuitNode, overwrite: bool = False):
        self.elements.setdefault(node.name, node)
        if isinstance(node, BusNode):
            self.network.add(
                node.type, node.name, v_nom=node.v_nom, overwrite=overwrite
            )
        elif isinstance(node, GeneratorNode):
            self.network.add(
                node.type,
                node.name,
                p_set=node.p_set,
                control=node.control,
                bus=node.busName,
                overwrite=overwrite,
            )
        elif isinstance(node, LoadNode):
            self.network.add(
                node.type,
                node.name,
                p_set=node.p_set,
                bus=node.busName,
                overwrite=overwrite,
            )
        elif isinstance(node, TransmissionLineNode):
            self.network.add(
                node.type,
                node.name,
                bus0=node.sourceBusName,
                bus1=node.targetBusName,
                x=node.x,
                r=node.r,
                overwrite=overwrite,
            )
        else:
            raise ValueError(f"Unknown node type: {node.type}")

    def removeElement(self, element: CircuitNode):
        # todo
        # handle disconnection
        pass

    def connect(self, sourceName: str, targetName: str) -> Tuple[bool, str]:
        sourceNode = self.elements.get(sourceName)
        targetNode = self.elements.get(targetName)
        if sourceNode is None or targetNode is None:
            print("Cannot connect non-existing elements")
            return (False, None)
        
        if not isinstance( sourceNode, BusNode) and not isinstance( targetNode, BusNode):
            print("Cannot connect non-bus elements")
            return (False, None)
        
        busNode : BusNode = None
        otherNode : CircuitNode = None
        if isinstance(sourceNode, BusNode):
            busNode = sourceNode
            otherNode = targetNode
        else:
            busNode = targetNode
            otherNode = sourceNode
        
        if isinstance( otherNode, BusNode):
            if(otherNode.name in busNode.connectionNames):
                print(f"Connection already exists between {busNode.name} and {otherNode.name}")
                return (False, None)

            busNode.connectionNames.append(otherNode.name)
            otherNode.connectionNames.append(busNode.name)
            line = TransmissionLineNode(0.1, 0.01, busNode.name, otherNode.name)    
            self.setNode(line)

            print(f"{line} created between {busNode.name} and {otherNode.name}")
            return (True, line.name)
      

        if isinstance(otherNode, GeneratorNode):
            if(otherNode.name in busNode.connectionNames):
                print(f"Connection already exists between {busNode.name} and {otherNode.name}")
                return (False, None)

            busNode.connectionNames.append(otherNode.name)
            otherNode.busName = busNode.name
            self.setNode(otherNode, overwrite=True)   
            print(f"{otherNode} connected to {busNode.name}")
            return (True, None)

        if isinstance(otherNode, LoadNode):
            if(otherNode.name in busNode.connectionNames):
                print(f"Connection already exists between {busNode.name} and {otherNode.name}")
                return (False, None)

            busNode.connectionNames.append(otherNode.name)
            otherNode.busName = busNode.name
            self.setNode(otherNode, overwrite=True)   
            print(f"{otherNode} connected to {busNode.name}")
            return (True, None)

        return (False, None)

    def runPowerFlow(self):
        self.network.pf()
        print("Power flow results:")
        print(self.network.lines_t.p0)
        print(self.network.buses_t.v_ang * 180 / np.pi)
        print(self.network.buses_t.v_mag_pu)


# def onElementLinked(board: BoardView, sourceNodeName: string, targetNodeName: string):
#     return onElementLinkedImpl(board, sourceNodeName, targetNodeName)
#     if not sourceNodeName.startswith("Bus") and not targetNodeName.startswith("Bus"):
#         print("Cannot link non-bus elements")
#         return (False,None)

#     if sourceNodeName.startswith("Bus") and targetNodeName.startswith("Bus"):
#         (line, _) = simulatorState.addElement("Line")
#         network.add("Line", line, bus0=sourceNodeName, bus1=targetNodeName, x=0.1, r=0.01)
#         print(f"{line} added between {sourceNodeName} and {targetNodeName}")
#         return (True,line)

#     if sourceNodeName.startswith("Bus") and targetNodeName.startswith("Generator"):
#         network.add(
#             "Generator",
#             targetNodeName,
#             bus=sourceNodeName,
#             p_set=100,
#             control="PQ",
#             overwrite=True,
#         )
#         print(f"{targetNodeName} added to {sourceNodeName}")
#         return (True,None)

#     if sourceNodeName.startswith("Generator") and targetNodeName.startswith("Bus"):
#         network.add(
#             "Generator",
#             sourceNodeName,
#             bus=targetNodeName,
#             p_set=100,
#             control="PQ",
#             overwrite=True,
#         )
#         print(f"{sourceNodeName} added to {targetNodeName}")
#         return (True,None)


#     if sourceNodeName.startswith("Bus") and targetNodeName.startswith("Load"):
#         network.add("Load", targetNodeName, bus=sourceNodeName, p_set=100, overwrite=True)
#         print(f"{targetNodeName} added to {sourceNodeName}")
#         return (True,None)

#     if sourceNodeName.startswith("Load") and targetNodeName.startswith("Bus"):
#         network.add("Load", sourceNodeName, bus=targetNodeName, p_set=100, overwrite=True)
#         print(f"{sourceNodeName} added to {targetNodeName}")
#         return (True,None)

#     return (False,None)
