from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout

from controllers.simulator_controller import SimulatorController
from view.board_view import BoardView
from view.bus_table import BusTable
from PySide6.QtWidgets import QSizePolicy

from view.line_table import LineTable


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        centralWidget = QWidget()
        self.setWindowTitle("Power Systems Simulator - Board")
        # Layout creation
        top_row = QHBoxLayout()
        bottom_row = QHBoxLayout()

        # Layout Alignment configuration
        top_row.setAlignment(Qt.AlignmentFlag.AlignLeft)
        bottom_row.setAlignment(Qt.AlignmentFlag.AlignLeft)

        clearStateButton = QPushButton("Clear All")
        clearStateButton.setFixedSize(70, 30)
        clearStateButton.setIconSize(QSize(70, 30))

        addBusButton = QPushButton("Add Bus")
        addBusButton.setFixedSize(70, 30)
        addBusButton.setIconSize(QSize(70, 30))

        show_buses_button = QPushButton("Buses")
        show_buses_button.setFixedSize(110, 30)

        show_lines_button = QPushButton("Lines")
        show_lines_button.setFixedSize(110, 30)

        show_y_bar_matrix_button = QPushButton("Y Bar Matrix")
        show_y_bar_matrix_button.setFixedSize(110, 30)

        runPowerFlowButton = QPushButton("Run Power Flow")
        runPowerFlowButton.setFixedSize(110, 30)

        # Create the board view.
        board = BoardView()

        # Screen montage
        column = QVBoxLayout(centralWidget)
        column.addLayout(top_row)
        column.addWidget(board)
        column.addLayout(bottom_row)

        simulatorInstance = SimulatorController.instance()

        # Connect button signal to the board's addSquare method.
        addBusButton.clicked.connect(lambda: simulatorInstance.addBus())
        runPowerFlowButton.clicked.connect(simulatorInstance.runPowerFlow)
        show_buses_button.clicked.connect(self.show_bus_window)
        show_lines_button.clicked.connect(self.show_line_window)
        clearStateButton.clicked.connect(simulatorInstance.clear_state)

        # Add widgets to the layout.
        top_row.addWidget(clearStateButton)
        top_row.addWidget(addBusButton)

        # Create a horizontal layout to place the board view on the left and a new widget on the right.

        bottom_row.addWidget(show_buses_button)
        bottom_row.addWidget(show_lines_button)
        bottom_row.addWidget(show_y_bar_matrix_button)
        bottom_row.addWidget(runPowerFlowButton)

        self.setCentralWidget(centralWidget)

    def show_bus_window(self):
        networkWindow = QMainWindow(parent=self)
        networkWindow.setWindowTitle("Bus Table")
        centralWidget = QWidget()
        layout = QVBoxLayout(centralWidget)
        layout.setContentsMargins(0, 0, 0, 0)

        busTable = BusTable()
        busTable.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        layout.addWidget(busTable)

        networkWindow.setCentralWidget(centralWidget)
        networkWindow.resize(800, 600)
        networkWindow.show()

    def show_line_window(self):
        lineWindow = QMainWindow(parent=self)
        lineWindow.setWindowTitle("Line Table")
        centralWidget = QWidget()
        layout = QVBoxLayout(centralWidget)
        layout.setContentsMargins(0, 0, 0, 0)

        rightWidget = LineTable()
        rightWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        layout.addWidget(rightWidget)

        lineWindow.setCentralWidget(centralWidget)
        lineWindow.resize(800, 600)
        lineWindow.show()
