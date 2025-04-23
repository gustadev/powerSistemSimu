

import time


class CircuitElement: 
    __counter = dict()
    def __init__(self, node_type: str, id: str, name: str = None):
        if id is None or name is None:
            generatedText = CircuitElement.__getCountForElement(node_type)

        self.type : str = node_type
        self.id : str = id if id else generatedText
        self.name : str = name if name else generatedText
    
    @staticmethod
    def __getCountForElement(node_type: str) -> str:
        if node_type not in CircuitElement.__counter:
            CircuitElement.__counter[node_type] = 0
        CircuitElement.__counter[node_type] += 1
        return f"{node_type[:2]}_{CircuitElement.__counter[node_type]}"

class CircuitNode(CircuitElement):
    def __init__(self, node_type: str, id: str, name: str = None, connectionIds: list[str] = []):
        super().__init__(node_type, id, name)
        self.connectionIds : list[str] = connectionIds

class ConnectionElement(CircuitElement):
    def __init__(self, node_type: str, id: str, name: str = None, sourceId: str = "", targetId: str = ""):
        super().__init__(node_type, id, name)
        self.sourceId: str = sourceId
        self.targetId: str = targetId

        