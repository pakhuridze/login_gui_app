import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.uic import loadUi
from converter import ConverterPage  # Import the ConverterPage class

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class Login(QDialog):
    def __init__(self):
        super().__init__()
        loadUi(resource_path('login.ui'), self)  # Use resource_path for loading UI
        self.loginbutton.clicked.connect(self.login_function)

    def login_function(self):
        email = self.email.text()
        password = self.password.text()
        if email == "admin" and password == "admin":
            self.open_converter_page()
        else:
            self.show_error_message("Invalid email or password")

    def show_error_message(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setText(message)
        error_dialog.setWindowTitle("Error")
        error_dialog.exec_()

    def open_converter_page(self):
        self.converter_page = ConverterPage(self)  # Pass the current login window instance
        self.converter_page.show()  # Show the ConverterPage
        self.close()  # Close the login page

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = Login()
    login_window.show()
    sys.exit(app.exec_())
