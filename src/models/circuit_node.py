import string
import time


class CircuitNode:
    counter = 0

    def __init__(self, node_type: str):
        self.id = CircuitNode.__getRandomId()
        self.type = node_type
        CircuitNode.counter += 1
        self.name = f"{node_type[:2]}_{CircuitNode.counter}"

    def __getRandomId():
        return hex(time.time_ns())[2:]


class BusNode(CircuitNode):
    def __init__(self, v_nom: float):
        super().__init__(f"Bus")
        self.v_nom: float = v_nom
        self.connectionIds: list[str] = []


class TransmissionLineNode(CircuitNode):
    def __init__(self, x: float, r: float, sourceId: str, targetId: str):
        super().__init__(f"Line")
        self.x: float = x
        self.r: float = r
        self.sourceId: str = sourceId
        self.targetId: str = targetId


class GeneratorNode(CircuitNode):
    def __init__(self, p_set: float, control: str, busId: str = None):
        super().__init__(f"Generator")
        self.p_set: float = p_set
        self.control: float = control
        self.busId = busId


class LoadNode(CircuitNode):
    def __init__(self, p_set: float, busId: str = None):
        super().__init__(f"Load")
        self.busId = busId
        self.p_set: float = p_set
