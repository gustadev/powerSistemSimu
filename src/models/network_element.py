from enum import Enum


class NetworkElement:
    __id_increment: dict[str, int] = dict[str, int]()

    def __init__(
        self,
        name: str,
        type: str,
        id: str | None = None,
    ):
        self.name: str = name
        if id is not None:
            self.__id: str = id
        else:
            if type not in NetworkElement.__id_increment:
                NetworkElement.__id_increment[type] = 0
            NetworkElement.__id_increment[type] += 1
            self.__id: str = f"{type}_{NetworkElement.__id_increment[type]}"

    @property
    def id(self) -> str:
        return self.__id


class ElementEvent(Enum):
    CREATED = "node_created"
    UPDATED = "wire_created"
    # DELETED = "wire_deleted" TODO implement component deletion
