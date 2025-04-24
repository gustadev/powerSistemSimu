
from enum import Enum


class ElementEvent(Enum):
    CREATED = "node_created"
    UPDATED = "wire_created"
    # DELETED = "wire_deleted" TODO implement component deletion