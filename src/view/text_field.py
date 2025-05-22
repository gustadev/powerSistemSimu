from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QHBoxLayout
from typing import Callable, cast
from PySide6.QtWidgets import QWidget, QLineEdit
from PySide6.QtCore import Qt


from typing import Generic, Type, TypeVar
from PySide6.QtGui import QFocusEvent


T = TypeVar("T", str, int, float)


class TextField(Generic[T], QWidget):
    def __init__(
        self,
        value: T | None = None,
        default_Value: T | None = None,
        title: str = "",
        type: Type[T] = str,
        trailing: str = "",
        enabled: bool = True,
        on_focus_out: Callable[[], None] | None = None,
    ):
        super().__init__()
        self.setEnabled(enabled)
        self.default_Value = default_Value
        self.title = title
        self.type = type
        self.field = QLineEdit()
        if value is not None:
            self.__set_value_string(value)
        self.label = QLabel(self.title)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.label)
        layout.addWidget(self.field)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        if trailing:
            layout.addWidget(QLabel(trailing))
        self.setLayout(layout)

        orig_focus_out_event = self.field.focusOutEvent

        def new_focus_out_event(event: QFocusEvent):
            orig_focus_out_event(event)
            self.__on_click_outside()

        self.field.focusOutEvent = new_focus_out_event
        self.on_focus_out = on_focus_out

    def getValue(self) -> T | None:
        try:
            text = self.field.text()
            if self.type == str:
                return cast(T, text)
            elif self.type == int and len(text) > 0:
                return cast(T, int(text))
            elif self.type == float and len(text) > 0:
                return cast(T, float(text))
            return None
        except:
            return None

    def setValue(self, value: T):
        self.__set_value_string(value)

    def clearValue(self):
        self.field.clear()

    def __on_click_outside(self):
        if self.on_focus_out is not None:
            self.on_focus_out()

    def __set_value_string(self, value: T) -> None:
        if self.type is float and isinstance(value, float):
            self.field.setText(f"{value:.4f}")
        elif self.type is float and isinstance(value, int):
            v = float(value)
            self.field.setText(f"{v:.4f}")
        else:
            self.field.setText(str(value))
