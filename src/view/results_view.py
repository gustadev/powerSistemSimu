from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QApplication
from PySide6.QtCore import Qt

class ResultsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Results")
        self.resize(600, 400)
        self.results = ""
        layout = QVBoxLayout(self)

        self.log_text = QTextEdit(self.results)
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        self.clear_button = QPushButton("Clean Logs", self)
        self.clear_button.clicked.connect(self.clear_logs)
        layout.addWidget(self.clear_button)

    def clear_logs(self):
        self.results = ""
        self.log_text.setText(self.results)
    
    def appendResult(self, res : str) : 
        self.results += res
        self.log_text.setText(self.results)

# Exemplo de uso independente
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ResultsView()
    window.append_log("Sistema iniciado.")
    window.append_log("Resultado do fluxo de potência: OK")
    window.show()
    sys.exit(app.exec())