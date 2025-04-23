from models.circuit_element import ConnectionElement


class TransmissionLineElement(ConnectionElement):
    def __init__(
        self,
        x: float = 1,
        r: float = 1,
        sourceId: str = None,
        targetId: str = None,
        id: str = None,
        name: str = None,
    ):
        super().__init__(
            node_type="Line", id=id, name=name, sourceId=sourceId, targetId=targetId
        )
        self.x: float = x
        self.r: float = r

    def copy(self):
        return TransmissionLineElement(
            x=self.x,
            r=self.r,
            sourceId=self.sourceId,
            targetId=self.targetId,
            id=self.id,
            name=self.name,
        )
