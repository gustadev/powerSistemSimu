from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
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
        layoutBtnElements = QHBoxLayout()
        layoutBtnActions = QHBoxLayout()
        horizontalLayout = QHBoxLayout()

        # Layout Alignment configuration
        layoutBtnElements.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layoutBtnActions.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Screen montage
        layout = QVBoxLayout(centralWidget)
        layout.addLayout(layoutBtnElements)
        layout.addLayout(horizontalLayout)
        layout.addLayout(layoutBtnActions)

        addBusButton = QPushButton("")  # ("Add Bus")
        addBusButton.setFixedSize(60, 35)
        addBusButton.setIcon(QIcon("assets/ico/busbar.png"))
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

        simulatorInstance = SimulatorController.instance()

        # Connect button signal to the board's addSquare method.
        addBusButton.clicked.connect(simulatorInstance.addBus)
        runPowerFlowButton.clicked.connect(simulatorInstance.runPowerFlow)
        show_buses_button.clicked.connect(self.show_bus_window)
        show_lines_button.clicked.connect(self.show_line_window)

        # Add widgets to the layout.
        layoutBtnElements.addWidget(addBusButton)
        layoutBtnElements.addWidget(board)

        # Create a horizontal layout to place the board view on the left and a new widget on the right.

        layoutBtnActions.addWidget(show_buses_button)
        layoutBtnActions.addWidget(show_lines_button)
        layoutBtnActions.addWidget(show_y_bar_matrix_button)
        layoutBtnActions.addWidget(runPowerFlowButton)

        self.setCentralWidget(centralWidget)

        self.show_bus_window()
        self.show_line_window()

    def show_bus_window(self):
        self.networkWindow = QMainWindow()
        self.networkWindow.setWindowTitle("Bus Table")
        centralWidget = QWidget()
        layout = QVBoxLayout(centralWidget)

        rightWidget = BusTable()
        rightWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        layout.addWidget(rightWidget)
        # horizontalLayout.setContentsMargins(5, 5, 5, 5)

        self.networkWindow.setCentralWidget(centralWidget)
        self.networkWindow.resize(800, 600)
        self.networkWindow.show()

        pass

    def show_line_window(self):
        self.lineWindow = QMainWindow()
        self.lineWindow.setWindowTitle("Line Table")
        centralWidget = QWidget()
        layout = QVBoxLayout(centralWidget)

        rightWidget = LineTable()
        rightWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        layout.addWidget(rightWidget)
        # horizontalLayout.setContentsMargins(5, 5, 5, 5)

        self.lineWindow.setCentralWidget(centralWidget)
        self.lineWindow.resize(800, 600)
        self.lineWindow.show()

        pass
