from models.circuit_element import CircuitNode


class BusNode(CircuitNode):
    def __init__(
        self,
        v_nom: float = 1,
        connectionIds: list[str] = [],
        id: str = None,
        name: str = None,
    ):
        super().__init__(id=id, name=name, node_type="Bus", connectionIds=connectionIds)
        self.v_nom: float = v_nom

    def copy(self):
        return BusNode(
            name=self.name,
            v_nom=self.v_nom,
            connectionIds=self.connectionIds.copy(),
            id=self.id,
        )
