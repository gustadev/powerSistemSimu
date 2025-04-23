

import time


class CircuitElement: 
    __counter = dict()
    def __init__(self, node_type: str, id: str, name: str = None):
        self.type : str = node_type
        self.id : str = None
        self.name : str = None

        if id:
            self.id = id
        else:
            self.id = hex(time.time_ns())[2:]

        if name:
            self.name = name
        else:
            if node_type not in CircuitElement.__counter:
                CircuitElement.__counter[node_type] = 0
            CircuitElement.__counter[node_type] += 1
            self.name = f"{node_type[:2]}_{CircuitElement.__counter[node_type]}"

class CircuitNode(CircuitElement):
    def __init__(self, node_type: str, id: str, name: str = None, connectionIds: list[str] = []):
        super().__init__(node_type, id, name)
        self.connectionIds : list[str] = connectionIds

class ConnectionElement(CircuitElement):
    def __init__(self, node_type: str, id: str, name: str = None, sourceId: str = "", targetId: str = ""):
        super().__init__(node_type, id, name)
        self.sourceId: str = sourceId
        self.targetId: str = targetId

        