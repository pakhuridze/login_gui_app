import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QComboBox, QPushButton, QLabel
from PyQt5.uic import loadUi

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class ConverterPage(QDialog):
    def __init__(self, main_window):
        super().__init__()
        loadUi(resource_path('converter.ui'), self)  # Load the converter UI file using resource_path

        # Reference to the main login window
        self.main_window = main_window

        # Find UI elements
        self.amountLineEdit = self.findChild(QLineEdit, 'amountLineEdit')
        self.fromCurrencyComboBox = self.findChild(QComboBox, 'fromCurrencyComboBox')
        self.toCurrencyComboBox = self.findChild(QComboBox, 'toCurrencyComboBox')
        self.convertButton = self.findChild(QPushButton, 'convertButton')
        self.resultLabel = self.findChild(QLabel, 'resultLabel')
        self.logoutButton = self.findChild(QPushButton, 'pushButton')  # Ensure this is the name used in the .ui file

        # Initially hide the result label
        self.resultLabel.setVisible(False)

        # Connect the convert button and logout button to their respective methods
        self.convertButton.clicked.connect(self.convert)
        self.logoutButton.clicked.connect(self.logout)

    def convert(self):
        try:
            # Get the amount from the line edit
            amount = float(self.amountLineEdit.text())

            # Get selected currencies
            from_currency = self.fromCurrencyComboBox.currentText()
            to_currency = self.toCurrencyComboBox.currentText()

            # Conversion rates
            exchange_rates = {
                'GEL_TO_USD': 1 / 2.5,
                'GEL_TO_EUR': 1 / 3.1,
                'EUR_TO_GEL': 3.1,
                'EUR_TO_USD': 3.1 / 2.5,
                'USD_TO_GEL': 2.5,
                'USD_TO_EUR': 2.5 / 3.1
            }

            # Determine the conversion rate key
            rate_key = f'{from_currency}_TO_{to_currency}'
            rate = exchange_rates.get(rate_key, 1)  # Default to 1 if rate is not found

            # Calculate the result
            result = amount * rate

            # Format the result with commas as thousand separators
            formatted_result = f'{result:,.2f} {to_currency}'

            # Show the result label and update its text
            self.resultLabel.setText(formatted_result)
            self.resultLabel.setVisible(True)

        except ValueError:
            self.resultLabel.setText("Invalid input")
            self.resultLabel.setVisible(True)

    def logout(self):
        self.close()  # Close the current converter window
        self.main_window.show()  # Show the main login window


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Initialize and show the login window
    from main import Login  # Import Login from main
    login_window = Login()
    login_window.show()

    sys.exit(app.exec_())
