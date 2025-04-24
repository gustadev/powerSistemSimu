from models.circuit_element import SingleConnectionElement


class LoadNode(SingleConnectionElement):
    def __init__(
        self,
        id: str = None,
        name: str = None,
        p_set: float = 1,
        connection_id: str = None,
    ):
        super().__init__(
            node_type="Load", id=id, name=name, connection_id=connection_id
        )
        self.__p_set: float = p_set

    @property
    def p_set(self) -> float:
        return self.__p_set

    def copyWith(
        self,
        p_set: float = None,
        connection_id: str = None,
        name: str = None,
    ):
        return LoadNode(
            name=name if name else self.name,
            p_set=p_set if p_set else self.p_set,
            connection_id=connection_id if connection_id else self.connection_id,
            id=self.id,
        )
