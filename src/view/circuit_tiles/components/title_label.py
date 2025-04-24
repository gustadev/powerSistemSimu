from PySide6.QtWidgets import QLabel


class TitleLabel(QLabel):
    def __init__(self, text: str):
        super().__init__(text=text)
        self.setStyleSheet("font-size: 16px; font-weight: bold;")
