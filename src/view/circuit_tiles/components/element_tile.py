from typing import *

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton


from typing import Generic, Type, TypeVar


from controllers.simulator_controller import SimulatorController
from enums.element_event import ElementEvent
from models.circuit_element import CircuitElement
from view.circuit_tiles.components.text_field import NotEmptyValidator, TextField
from view.circuit_tiles.components.title_label import TitleLabel


E = TypeVar("Type", bound=CircuitElement)


class ElementTile(Generic[E], QWidget):
    def __init__(self, element: CircuitElement, type: Type[E]):
        super().__init__()
        self.type: Type[E] = type
        self.__element: E = element
        simulatorInstance = SimulatorController.instance()
        simulatorInstance.listen(self.circuitListener)
        self.build_widget()
        self.update_form_values()

    @property
    def element(self) -> E:
        return self.__element

    def circuitListener(self, element: CircuitElement, event: ElementEvent):
        if (
            event == ElementEvent.UPDATED
            and element.id == self.element.id
            and isinstance(element, self.type)
        ):
            self.__element = element
            self.update_form_values()

    def update_form_values(self):
        self.nameField.setValue(self.element.name)

    def build_widget(self):
        layout = QVBoxLayout(self)
        self._pending_title = TitleLabel(self.element.type)
        layout.addWidget(self._pending_title)

        self.build_form(layout)

        self.submit_button = QPushButton("Edit")
        self.submit_button.clicked.connect(self.edit)
        layout.addWidget(self.submit_button)

    def build_form(self, layout: QVBoxLayout):
        self.nameField = TextField(
            title="name", type=str, validators=[NotEmptyValidator()]
        )
        layout.addWidget(self.nameField)

    def edit(self):
        pass
