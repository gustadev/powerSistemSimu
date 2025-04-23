from typing import *
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
)
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer

from models.load import LoadNode


class LoadTile(QWidget):
    def __init__(self, node: LoadNode):
        super().__init__()
        self.node: LoadNode = node

        self._pending_title = QLabel(self.node.type)
        self._pending_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        QTimer.singleShot(0, lambda: self.layout().insertWidget(0, self._pending_title))

        layout = QVBoxLayout(self)
        self.nameField = QLineEdit()
        self.nameField.setPlaceholderText("Name")
        self.nameField.setText(node.name)
        layout.addWidget(self.nameField)

        self.powerField = QLineEdit()
        self.powerField.setPlaceholderText("Power")
        self.powerField.setText(str(node.p_set))
        layout.addWidget(self.powerField)

        def _submit_node_edition():
            copy = self.node.copy()
            copy.name = self.nameField.text()
            pass

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(_submit_node_edition)
        layout.addWidget(self.submit_button)
