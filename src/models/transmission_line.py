from models.circuit_element import DoubleConnectionElement


class TransmissionLineElement(DoubleConnectionElement):
    def __init__(
        self,
        reactance: float = 1,
        resistance: float = 1,
        source_id: str = None,
        target_id: str = None,
        id: str = None,
        name: str = None,
    ):
        super().__init__(
            node_type="Line", id=id, name=name, source_id=source_id, target_id=target_id
        )
        self.__reactance: float = reactance
        self.__resistance: float = resistance

    @property
    def reactance(self) -> float:
        return self.__reactance
    
    @property
    def resistance(self) -> float:
        return self.__resistance

    def copyWith(
        self,
        reactance: float = None,
        resistance: float = None,
        source_id: str = None,
        target_id: str = None,
        name: str = None,
    ):
        return TransmissionLineElement(
            name=name if name else self.name,
            reactance=reactance if reactance else self.reactance,
            resistance=resistance if resistance else self.resistance,
            source_id=source_id if source_id else self.source_id,
            target_id=target_id if target_id else self.target_id,
            id=self.id,
        )
