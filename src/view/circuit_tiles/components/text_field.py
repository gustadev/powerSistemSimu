from typing import *

from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QHBoxLayout
from typing import cast
from PySide6.QtWidgets import QWidget, QLineEdit


from typing import Generic, Type, TypeVar


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


T = TypeVar("Type", str, int, float)


class TextField(Generic[T], QWidget):
    def __init__(
        self,
        title: str,
        value: T = None,
        type: Type[T] = str,
        trailing: str = "",
        enabled: bool = True,
        validators: list[TextValidator] = [NotEmptyValidator()],
    ):
        super().__init__()
        self.setEnabled(enabled)
        self.title = title
        self.type = type
        self.validators = validators
        self.field = QLineEdit()
        self.field.setText(str(value))
        layout = QHBoxLayout(self)
        layout.addWidget(QLabel(title))
        layout.addWidget(self.field)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        if trailing:
            layout.addWidget(QLabel(trailing))
        self.setLayout(layout)

    def getValue(self) -> T:
        text = self.field.text()
        if self.type == str:
            return text
        elif self.type == int:
            return cast(T, int(text))
        elif self.type == float:
            return cast(T, float(text))

    def setValue(self, value: T):
        self.field.setText(str(value))

    def validate(self) -> bool:
        text = self.field.text()
        for validator in self.validators:
            result = validator.validate(title=self.title, value=text)
            if result:
                return False
        return True
