from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QHBoxLayout
from typing import Callable, cast
from PySide6.QtWidgets import QWidget, QLineEdit
from PySide6.QtCore import Qt


from typing import Generic, Type, TypeVar
from PySide6.QtGui import QFocusEvent


class TextValidator:
    def validate(self, title: str, value: str) -> str | None:
        pass


class NotEmptyValidator(TextValidator):
    def validate(self, title: str, value: str) -> str | None:
        if not value.strip():
            return f"{title} cannot be empty"
        return None


class NumberValidator(TextValidator):
    def __init__(self, min: float | None = None, max: float | None = None):
        self.min = min
        self.max = max

    def validate(self, title: str, value: str) -> str | None:
        try:
            number = float(value)
            if self.min is not None and number < self.min:
                return f"{title} must be greater than {self.min}"
            if self.max is not None and number > self.max:
                return f"{title} must be less than {self.max}"
            return None

        except ValueError:
            return f"{title} must be a number"


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
        validators: list[TextValidator] = [NotEmptyValidator()],
        on_focus_out: Callable[[], None] | None = None,
    ):
        super().__init__()
        self.setEnabled(enabled)
        self.default_Value = default_Value
        self.title = title
        self.type = type
        self.validators = validators
        self.field = QLineEdit()
        # self.field.setFixedSize(QSize(50,30))
        if value is not None:
            self.field.setText(str(value))
        self.label = QLabel(self.title)
        # self.label.setFixedSize(QSize(50,30))
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

    def validate(self) -> bool:
        text = self.field.text()
        for validator in self.validators:
            result = validator.validate(title=self.title, value=text)
            if result:
                return False
        return True

    def __on_click_outside(self):
        if self.on_focus_out is not None:
            self.on_focus_out()

    def __set_value_string(self, value: T) -> None:
        if self.type is float and isinstance(value, float):
            self.field.setText(f"{value:8.4f}")
        else:
            self.field.setText(str(value))
