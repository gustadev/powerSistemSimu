from models.circuit_element import DoubleConnectionElement


class WireElement(DoubleConnectionElement):
    def __init__(
        self,
        source_id: str,
        target_id: str,
        id: str = None,
        name: str = None,
    ):
        super().__init__(
            node_type="Wire", id=id, name=name, source_id=source_id, target_id=target_id
        )
