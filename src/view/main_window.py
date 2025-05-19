from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout

from controllers.simulator_controller import SimulatorController
from view.board_view import BoardView
from view.element_list import ElementList
from PySide6.QtWidgets import QSizePolicy


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        centralWidget = QWidget()
        self.setWindowTitle("Power Systems Simulator")
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

        show_network_button = QPushButton("Edit Network")
        show_network_button.setFixedSize(110, 30)

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
        show_network_button.clicked.connect(self.show_network_window)

        # Add widgets to the layout.
        layoutBtnElements.addWidget(addBusButton)
        layoutBtnElements.addWidget(board)

        # Create a horizontal layout to place the board view on the left and a new widget on the right.

        layoutBtnActions.addWidget(runPowerFlowButton)
        layoutBtnActions.addWidget(show_network_button)
        layoutBtnActions.addWidget(show_y_bar_matrix_button)

        self.setCentralWidget(centralWidget)

        self.show_network_window()

    def show_network_window(self):
        self.networkWindow = QMainWindow()
        self.networkWindow.setWindowTitle("Network")
        centralWidget = QWidget()
        layout = QVBoxLayout(centralWidget)

        rightWidget = ElementList()
        rightWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        layout.addWidget(rightWidget)
        # horizontalLayout.setContentsMargins(5, 5, 5, 5)

        self.networkWindow.setCentralWidget(centralWidget)
        self.networkWindow.resize(800, 600)
        self.networkWindow.show()

        pass
