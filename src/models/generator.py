from models.circuit_element import CircuitNode


class GeneratorNode(CircuitNode):
    def __init__(
        self,
        id: str = None,
        name: str = None,
        nominalPower: float = 1,
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
        self.nominalPower: float = nominalPower

    def getBusId(self) -> str | None:
        return self.connectionIds[0] if len(self.connectionIds) > 0 else None

    def copy(self):
        return GeneratorNode(
            name=self.name,
            nominalPower=self.nominalPower,
            control=self.control,
            busId=self.connectionIds[0] if len(self.connectionIds) > 0 else None,
            id=self.id,
        )
