from enum import Enum


class NetworkElement:
    __id_increment: int = 0

    def __init__(self, name: str, id: int | None = None):
        self.name: str = name
        if id:
            self.__id: int = id
        else:
            self.__id: int = NetworkElement.__id_increment
            NetworkElement.__id_increment += 1

    @property
    def id(self) -> int:
        return self.__id


class ElementEvent(Enum):
    CREATED = "node_created"
    UPDATED = "wire_created"
    # DELETED = "wire_deleted" TODO implement component deletion
