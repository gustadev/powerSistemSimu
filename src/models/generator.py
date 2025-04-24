from models.circuit_element import SingleConnectionElement


class GeneratorNode(SingleConnectionElement):
    def __init__(
        self,
        id: str = None,
        name: str = None,
        nominal_power: float = 1,
        control: str = "GM",
        connection_id: str = None,
    ):
        super().__init__(
            node_type="Generator", id=id, name=name, connection_id=connection_id
        )
        self.__control: str = control
        self.__nominal_power: float = nominal_power

    @property
    def control(self) -> str:
        return self.__control

    @property
    def nominal_power(self) -> float:
        return self.__nominal_power

    def copyWith(
        self,
        control: str = None,
        nominal_power: float = None,
        connection_id: str = None,
        name: str = None,
    ):
        return GeneratorNode(
            name=name if name else self.name,
            control=control if control else self.control,
            nominal_power=nominal_power if nominal_power else self.nominal_power,
            connection_id=connection_id if connection_id else self.connection_id,
            id=self.id,
        )
