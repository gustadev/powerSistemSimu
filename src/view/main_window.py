from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy

from controllers.simulator_controller import SimulatorController
from view.board_view import BoardView
from view.bus_table import BusTable
# from view.results_view import ResultsView

from view.line_table import LineTable


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        centralWidget = QWidget()
        simulatorInstance = SimulatorController.instance()
        self.setWindowTitle("Power Systems Simulator - Board")
        # Layout creation
        layoutBtnElements = QVBoxLayout()
        layoutBtnActions = QHBoxLayout()
        horizontalLayout = QHBoxLayout()

        toolbar = self.menuBar()

        view = toolbar.addMenu("View")
        viewBars = QAction("Bars",view)
        viewBars.triggered.connect(self.show_bus_window)
        view.addAction(viewBars)

        viewLine = QAction("Lines",view)
        viewLine.triggered.connect(self.show_line_window)
        view.addAction(viewLine)

        viewLine = QAction("Results",view)
        viewLine.triggered.connect(simulatorInstance.showResults)
        view.addAction(viewLine)

        show = toolbar.addMenu("Show")
        showYMatrix = QAction("Y Matrix",show)
        # showYMatrix.triggered.connect(self.)
        show.addAction(showYMatrix)

        run = toolbar.addMenu("Run")
        runLoadFlow = QAction("Load Flow",run)
        runLoadFlow.triggered.connect(SimulatorController.instance().runPowerFlow)
        run.addAction(runLoadFlow)

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

        # show_buses_button = QPushButton("Buses")
        # show_buses_button.setFixedSize(110, 30)

        # show_lines_button = QPushButton("Lines")
        # show_lines_button.setFixedSize(110, 30)

        # show_y_bar_matrix_button = QPushButton("Y Bar Matrix")
        # show_y_bar_matrix_button.setFixedSize(110, 30)

        # runPowerFlowButton = QPushButton("Run Power Flow")
        # runPowerFlowButton.setFixedSize(110, 30)

        # Create the board view.
        board = BoardView()

        # Connect button signal to the board's addSquare method.
        addBusButton.clicked.connect(lambda: simulatorInstance.addBus())
        # runPowerFlowButton.clicked.connect(simulatorInstance.runPowerFlow)
        # show_buses_button.clicked.connect(self.show_bus_window)
        # show_lines_button.clicked.connect(self.show_line_window)

        # Add widgets to the layout.
        layoutBtnElements.addWidget(addBusButton)
        layoutBtnElements.addWidget(board)

        # Create a horizontal layout to place the board view on the left and a new widget on the right.

        # layoutBtnActions.addWidget(show_buses_button)
        # layoutBtnActions.addWidget(show_lines_button)
        # layoutBtnActions.addWidget(show_y_bar_matrix_button)
        # layoutBtnActions.addWidget(runPowerFlowButton)

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

