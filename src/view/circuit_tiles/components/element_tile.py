from PySide6.QtWidgets import QWidget, QHBoxLayout

from typing import Generic, Type, TypeVar

from controllers.simulator_controller import SimulatorController
from models.network_element import ElementEvent, NetworkElement


E = TypeVar("E", bound=NetworkElement)


class ElementTile(Generic[E], QWidget):
    def __init__(self, element: E, type: Type[E]):
        super().__init__()
        self.type: Type[E] = type
        self.__element: E = element
        SimulatorController.instance().listen(self.circuitListener)
        self.build_widget()
        self.update_form_values()

    @property
    def element(self) -> E:
        return self.__element

    def circuitListener(self, element: NetworkElement, event: ElementEvent):
        if (
            event == ElementEvent.UPDATED
            and element.id == self.element.id
            and isinstance(element, self.type)
        ):
            self.__element = element
            self.update_form_values()

    def update_form_values(self):
        pass

    def build_widget(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.build_form(layout)

    def build_form(self, layout: QHBoxLayout):
        pass

    def validate(self) -> bool:
        raise NotImplementedError("validate method not implemented")

    def save(self) -> None:
        raise NotImplementedError("save method not implemented")
