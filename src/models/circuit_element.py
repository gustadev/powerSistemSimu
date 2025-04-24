# General circuit element class
class CircuitElement:
    __counter = dict()

    def __init__(self, node_type: str, id: str, name: str = None):
        if id is None or name is None:
            generatedText = CircuitElement.__getCountForElement(node_type)

        self.__type: str = node_type
        self.__id: str = id if id else generatedText
        self.__name: str = name if name else generatedText

    @staticmethod
    def __getCountForElement(node_type: str) -> str:
        if node_type not in CircuitElement.__counter:
            CircuitElement.__counter[node_type] = 0
        CircuitElement.__counter[node_type] += 1
        return f"{node_type[:2]}_{CircuitElement.__counter[node_type]}"

    @property
    def type(self) -> str:
        return self.__type

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name


class ManyConnectionsElement(CircuitElement):
    def __init__(
        self, node_type: str, id: str, name: str = None, connection_ids: tuple[str] = []
    ):
        super().__init__(node_type, id, name)
        self.__connection_ids: tuple[str] = connection_ids

    @property
    def connection_ids(self) -> tuple[str]:
        return tuple(self.__connection_ids)


class DoubleConnectionElement(CircuitElement):
    def __init__(
        self,
        node_type: str,
        id: str,
        name: str = None,
        source_id: str = "",
        target_id: str = "",
    ):
        super().__init__(node_type, id, name)
        self.__sourceId: str = source_id
        self.__targetId: str = target_id

    @property
    def source_id(self) -> str:
        return self.__sourceId

    @property
    def target_id(self) -> str:
        return self.__targetId


class SingleConnectionElement(CircuitElement):
    def __init__(
        self,
        node_type: str,
        id: str,
        name: str = None,
        connection_id: str | None = None,
    ):
        super().__init__(node_type, id, name)
        self.__connectionId: str | None = connection_id

    @property
    def connection_id(self) -> str | None:
        return self.__connectionId
