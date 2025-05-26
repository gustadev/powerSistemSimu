from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QSizePolicy,
)

from controllers.simulator_controller import SimulatorController
from view.board_view import BoardView
from view.bus_table import BusTable


from view.line_table import LineTable
from view.text_field import TextField


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        centralWidget = QWidget()
        simulatorInstance = SimulatorController.instance()
        self.setWindowTitle("Power Systems Simulator - Board")
        # Layout creation
        top_row = QHBoxLayout()
        bottom_row = QHBoxLayout()

        toolbar = self.menuBar()
        toolbar.setNativeMenuBar(False)

        view = toolbar.addMenu("View")
        viewBars = QAction("Bars", view)
        viewBars.triggered.connect(self.show_bus_window)
        view.addAction(viewBars)

        viewLine = QAction("Lines", view)
        viewLine.triggered.connect(self.show_line_window)
        view.addAction(viewLine)

        viewLine = QAction("Results", view)
        viewLine.triggered.connect(simulatorInstance.showResults)
        view.addAction(viewLine)

        show = toolbar.addMenu("Show")
        showYMatrix = QAction("Y Matrix", show)

        show.addAction(showYMatrix)

        run = toolbar.addMenu("Run")
        runLoadFlow = QAction("Load Flow", run)
        runLoadFlow.triggered.connect(SimulatorController.instance().runPowerFlow)
        run.addAction(runLoadFlow)

        # Layout Alignment configuration
        top_row.setAlignment(Qt.AlignmentFlag.AlignLeft)
        bottom_row.setAlignment(Qt.AlignmentFlag.AlignLeft)

        importFileButton = QPushButton("Import")
        importFileButton.setFixedSize(70, 30)

        expoerFileButton = QPushButton("Export")
        expoerFileButton.setFixedSize(70, 30)

        importIeeeFileButton = QPushButton("Import IEEE")
        importIeeeFileButton.setFixedSize(120, 30)

        clearStateButton = QPushButton("Clear All")
        clearStateButton.setFixedSize(70, 30)
        clearStateButton.setIconSize(QSize(70, 30))

        addBusButton = QPushButton("Add Bus")
        addBusButton.setFixedSize(70, 30)
        addBusButton.setIconSize(QSize(70, 30))

        # show_buses_button = QPushButton("Buses")
        # show_buses_button.setFixedSize(110, 30)

        # show_lines_button = QPushButton("Lines")
        # show_lines_button.setFixedSize(110, 30)

        show_y_bar_matrix_button = QPushButton("Print Network")
        show_y_bar_matrix_button.setFixedSize(110, 30)

        # runPowerFlowButton = QPushButton("Run Power Flow")
        # runPowerFlowButton.setFixedSize(110, 30)

        self.powerBaseField = TextField[int](
            type=int,
            title="base",
            trailing="MVA",
            on_focus_out=self.on_power_base_changed,
            value=int(SimulatorController.instance().power_base_mva),
        )

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
        clearStateButton.clicked.connect(simulatorInstance.clear_state)
        importFileButton.clicked.connect(board.import_json)
        expoerFileButton.clicked.connect(board.export_json)
        importIeeeFileButton.clicked.connect(board.import_ieee)
        show_y_bar_matrix_button.clicked.connect(self.print_network)

        # Add widgets to the layout.
        top_row.addWidget(self.powerBaseField)
        top_row.addWidget(importFileButton)
        top_row.addWidget(expoerFileButton)
        top_row.addWidget(importIeeeFileButton)
        top_row.addWidget(clearStateButton)

        # Create a horizontal layout to place the board view on the left and a new widget on the right.

        bottom_row.addWidget(addBusButton)
        bottom_row.addWidget(show_y_bar_matrix_button)

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

    def print_network(self):
        SimulatorController.instance().printNetwork()

    def on_power_base_changed(self):
        controller = SimulatorController.instance()
        powerBase = self.powerBaseField.getValue()
        if powerBase == None or powerBase <= 0:
            controller = SimulatorController.instance()
            self.powerBaseField.setValue(int(controller.power_base_mva))
            return
        controller.power_base_mva = float(powerBase)

    # def show_results(self):
    #     resultsWindow = QMainWindow(parent=self)
    #     resultsWindow.setWindowTitle("Results")
    #     centralWidget = QWidget()
    #     layout = QVBoxLayout(centralWidget)
    #     layout.setContentsMargins(0, 0, 0, 0)

    #     rightWidget = ResultsView()
    #     rightWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    #     layout.addWidget(rightWidget)

    #     resultsWindow.setCentralWidget(centralWidget)
    #     resultsWindow.resize(800, 600)
    #     resultsWindow.show()
