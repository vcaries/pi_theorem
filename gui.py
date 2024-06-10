"""
    This module contains the GUI for the Pi Theorem Calculator.

    Example usage:
        python gui.py

    author: V. Caries (creator)
"""


# Import necessary packages
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QTextEdit, QMessageBox, QHeaderView
from PyQt5.QtCore import Qt
from pi_theorem import apply_pi_theorem


class PiTheoremApp(QMainWindow):
    """
        Main application window for the Pi Theorem Calculator.

        This class handles the creation and management of the GUI, as well as the interaction
        with the pi theorem calculations.

        Inherits:
            QMainWindow: The main window class from PyQt5.

        Attributes:
            variables (dict): A dictionary to store variables and their dimensions.
            table (QTableWidget): A table to display the variables.
            var_name (QLineEdit): A text input for the variable name.
            var_m (QLineEdit): A text input for the M dimension.
            var_l (QLineEdit): A text input for the L dimension.
            var_t (QLineEdit): A text input for the T dimension.
            add_button (QPushButton): A button to add a variable.
            calculate_button (QPushButton): A button to calculate the Pi terms.
            result_label (QLabel): A label for the result.
            result_text (QTextEdit): A text area to display the dimensionless numbers.
        """
    def __init__(self):
        """
            Initializes the main application window and its components.
        """
        # Call the parent class constructor
        super().__init__()

        # Initialize the attributes
        self.variables: dict = {}  # Dictionary to store variables and their dimensions
        self.table: QTableWidget = None
        self.var_name: QLineEdit = None
        self.var_m: QLineEdit = None
        self.var_l: QLineEdit = None
        self.var_t: QLineEdit = None
        self.add_button: QPushButton = None
        self.calculate_button: QPushButton = None
        self.result_label: QLabel = None
        self.result_text: QTextEdit = None

        # Initialize the user interface
        self.init_UI()

    def init_UI(self) -> None:
        """
            Initialize the user interface of the application.
        """
        self.setWindowTitle('Pi Theorem Calculator')  # Set the window title
        self.setGeometry(100, 100, 600, 400)  # Set a default size for the window (x, y, width, height)

        # Create the central widget and the main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Create the table to display the variables
        self.table = QTableWidget(0, 4)  # Table with 4 columns
        self.table.setHorizontalHeaderLabels(['Variable', 'M', 'L', 'T'])  # Set the column headers
        main_layout.addWidget(self.table)  # Add the table to the main layout

        # Center the labels of the table
        header = self.table.horizontalHeader()
        for i in range(self.table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
            header.setDefaultAlignment(Qt.AlignCenter)

        # Create the input fields for adding variables
        add_layout = QHBoxLayout()
        main_layout.addLayout(add_layout)

        # Add the input fields and the 'Add Variable' button
        add_layout.addWidget(QLabel('Variable'))
        self.var_name = QLineEdit()
        add_layout.addWidget(self.var_name)

        # Add the input fields for the dimensions
        add_layout.addWidget(QLabel('M'))
        self.var_m = QLineEdit()
        add_layout.addWidget(self.var_m)
        add_layout.addWidget(QLabel('L'))
        self.var_l = QLineEdit()
        add_layout.addWidget(self.var_l)
        add_layout.addWidget(QLabel('T'))
        self.var_t = QLineEdit()
        add_layout.addWidget(self.var_t)

        # Add the 'Add Variable' button
        self.add_button = QPushButton('Add Variable')
        self.add_button.clicked.connect(self.add_variable)
        add_layout.addWidget(self.add_button)

        # Create the 'Calculate Pi Terms' button
        self.calculate_button = QPushButton('Calculate Pi Terms')
        self.calculate_button.clicked.connect(self.calculate_pi_terms)
        main_layout.addWidget(self.calculate_button)

        # Create the label and text area for the result
        self.result_label = QLabel('Dimensionless Numbers:')
        main_layout.addWidget(self.result_label)
        self.result_text = QTextEdit()
        main_layout.addWidget(self.result_text)

    def add_variable(self) -> None:
        """
            Add a variable to the table of variables.
        """
        # Get the input values from the text fields
        var_name = self.var_name.text().strip()
        try:
            var_m = int(self.var_m.text().strip())
            var_l = int(self.var_l.text().strip())
            var_t = int(self.var_t.text().strip())

        except ValueError:
            QMessageBox.critical(self, 'Input Error', 'Dimensions must be integers')
            return

        # Check if the variable name is valid and not already in the dictionary
        if var_name and var_name not in self.variables:
            # Add the variable to the dictionary
            self.variables[var_name] = [var_m, var_l, var_t]

            # Add the variable to the table
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            item = QTableWidgetItem(var_name)
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_position, 0, item)
            item = QTableWidgetItem(str(var_m))
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_position, 1, item)
            item = QTableWidgetItem(str(var_l))
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_position, 2, item)
            item = QTableWidgetItem(str(var_t))
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_position, 3, item)

            # Clear the input fields
            self.var_name.clear()
            self.var_m.clear()
            self.var_l.clear()
            self.var_t.clear()

        else:
            QMessageBox.critical(self, 'Input Error', 'Invalid variable name or variable already exists')

    def calculate_pi_terms(self) -> None:
        """
            Calculate the dimensionless Pi terms using the Pi theorem.
        """
        try:
            # Apply the Pi theorem to the variables
            pi_terms = apply_pi_theorem(self.variables, output=True)

            # Clear the text area
            self.result_text.clear()

            # Display the dimensionless numbers
            for i, pi_term in enumerate(pi_terms, 1):
                centered_text = f'<div style="text-align: center;"><pre>Pi_{i} = {pi_term}</pre></div>'  # Center the text
                self.result_text.append(centered_text)

        except ValueError as e:
            QMessageBox.critical(self, 'Calculation Error', str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PiTheoremApp()
    window.show()
    sys.exit(app.exec_())