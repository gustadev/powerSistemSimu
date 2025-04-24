from models.circuit_element import ManyConnectionsElement


class BusNode(ManyConnectionsElement):
    def __init__(
        self,
        v_nom: float = 1,
        connection_ids: tuple[str] = tuple[str](),
        id: str = None,
        name: str = None,
    ):
        super().__init__(
            id=id, name=name, node_type="Bus", connection_ids=connection_ids
        )
        self.__v_nom: float = v_nom

    @property
    def v_nom(self) -> float:
        return self.__v_nom

    def copyWith(
        self,
        v_nom: float = None,
        connection_ids: tuple[str] = None,
        name: str = None,
    ):
        return BusNode(
            name=name if name else self.name,
            v_nom=v_nom if v_nom else self.v_nom,
            connection_ids=(connection_ids if connection_ids else self.connection_ids),
            id=self.id,
        )
