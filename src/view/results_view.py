from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QApplication
from PySide6.QtCore import Qt
from controllers.simulator_controller import SimulatorController

class ResultsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Results de Resultados")
        self.resize(600, 400)
        self.results = SimulatorController.instance().get_results()
        layout = QVBoxLayout(self)

        self.log_text = QTextEdit(self.results)
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        self.clear_button = QPushButton("Limpar Resultss", self)
        self.clear_button.clicked.connect(self.clear_logs)
        layout.addWidget(self.clear_button)

    def clear_logs(self):
        SimulatorController.instance().clear_results()
        

# Exemplo de uso independente
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ResultsView()
    window.append_log("Sistema iniciado.")
    window.append_log("Resultado do fluxo de potência: OK")
    window.show()
    sys.exit(app.exec())