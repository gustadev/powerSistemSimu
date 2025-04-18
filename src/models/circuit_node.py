import string


class CircuitNode:
    def __init__(self, name: str, node_type: str):
        self.name = name
        self.type = node_type


class BusNode(CircuitNode):
    counter = 0

    def __init__(self, v_nom: float):
        BusNode.counter += 1
        super().__init__(f"Bus {BusNode.counter}", f"Bus")
        self.v_nom: float = v_nom
        self.connectionNames: list[CircuitNode] = []


class TransmissionLineNode(CircuitNode):
    counter = 0

    def __init__(self, x: float, r: float, sourceBusName: str, targetBusName: str):
        TransmissionLineNode.counter += 1
        super().__init__(f"Line {TransmissionLineNode.counter}", f"Line")
        self.x: float = x
        self.r: float = r
        self.sourceBusName: str = sourceBusName
        self.targetBusName: str = targetBusName


class GeneratorNode(CircuitNode):
    counter = 0

    def __init__(self, p_set: float, control: str, bus: str = None):
        GeneratorNode.counter += 1
        super().__init__(f"Gen {GeneratorNode.counter}", f"Generator")
        self.p_set: float = p_set
        self.control: float = control
        self.busName = None | str


class LoadNode(CircuitNode):
    counter = 0

    def __init__(self, p_set: float, bus: str = None):
        LoadNode.counter += 1
        super().__init__(f"Load {LoadNode.counter}", f"Load")
        self.busName = None | str
        self.p_set: float = p_set
