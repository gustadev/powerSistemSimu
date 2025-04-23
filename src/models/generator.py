from models.circuit_element import CircuitNode


class GeneratorNode(CircuitNode):
    def __init__(
        self,
        id: str = None,
        name: str = None,
        p_set: float = 1,
        control: str = "GM",
        busId: str = None,
    ):
        super().__init__(
            node_type="Generator",
            id=id,
            name=name,
            connectionIds=[busId] if busId else [],
        )
        self.control: str = control
        self.p_set: float = p_set

    def getBusId(self) -> str | None:
        return self.connectionIds[0] if len(self.connectionIds) > 0 else None

    def copy(self):
        return GeneratorNode(
            name=self.name,
            p_set=self.p_set,
            control=self.control,
            busId=self.connectionIds[0] if len(self.connectionIds) > 0 else None,
            id=self.id,
        )
