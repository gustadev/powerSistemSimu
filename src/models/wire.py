from models.circuit_element import ConnectionElement


class WireElement(ConnectionElement):
    def __init__(
        self,
        sourceId: str,
        targetId: str,
        id: str = None,
        name: str = None,
    ):
        super().__init__(
            node_type="Wire", id=id, name=name, sourceId=sourceId, targetId=targetId
        )

    def copy(self):
        return WireElement(
            sourceId=self.sourceId,
            targetId=self.targetId,
            id=self.id,
            name=self.name,
        )
