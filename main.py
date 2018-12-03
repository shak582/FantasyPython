import sys
from PyQt5 import QtWidgets, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Global Variables for stack index
LOGIN_REGISTER = 0
HOME = 1

#comment 

# To change between Pages - self.parent().setCurrentIndex(HOME)
#          Changes depending on what you want to switch to ^
class LoginRegisterWidget(QtWidgets.QWidget):  # Normal LoginPage
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.setup()

    def setup(self):
        # Our Layout
        self.box_layout = QtWidgets.QVBoxLayout()
        # Login Button
        self.login_button = QtWidgets.QPushButton("Login", self)
        self.login_button.clicked.connect(self.login_click)

        # Register Button
        self.register_button = QtWidgets.QPushButton("Register", self)
        self.register_button.clicked.connect(self.register_click)

        # Adding buttons to layout
        self.box_layout.addWidget(self.login_button)
        self.box_layout.addWidget(self.register_button)

        self.setLayout(self.box_layout)

    def login_click(self):
        self.login_dialog = QDialog()
        self.login_dialog.setWindowTitle("Login")
        self.login_dialog.exec_()

    def register_click(self):
        self.register_dialog = QDialog()
        self.register_dialog.setWindowTitle("Register")
        self.register_dialog.exec_()


class HomeWidget(QtWidgets.QWidget): # HomeWidget for joining, creating match
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.setup()

    def setup(self):
        # Our Layout
        self.box_layout = QtWidgets.QVBoxLayout()
        # Create Match Button
        self.create_button = QtWidgets.QPushButton("Create Match", self)
        self.create_button.clicked.connect(self.create_click)

        # Join Match Button
        self.join_button = QtWidgets.QPushButton("Join Match", self)
        self.join_button.clicked.connect(self.join_click)

        # Current Match Button
        self.current_button = QtWidgets.QPushButton("Current Match", self)
        self.current_button.clicked.connect(self.current_click)

        # Adding buttons to layout
        self.box_layout.addWidget(self.create_button)
        self.box_layout.addWidget(self.join_button)
        self.box_layout.addWidget(self.current_button)

        self.setLayout(self.box_layout)

    def create_click(self):
        self.garbage = 0

    def join_click(self):
        self.garbage = 0

    def current_click(self):
        self.garbage = 0

# INDEXES FOR STACK
# 0 - LoginRegisterWidget
# 1 - HomeWidget

class MainWindow(QtWidgets.QMainWindow):  # Main Window
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setup()

    def setup(self):
        self.setGeometry(0, 0, 700, 700)
        self.setFixedSize(700, 700)  # eliminating resizing
        self.setWindowTitle("Fantasy Football")

        self.PageStack = QStackedWidget(self)

        # Creating our pages for the stack
        self.main_page = LoginRegisterWidget(self)
        self.home_page = HomeWidget(self)

        # Adding to stack; Pages indexed in order of addition
        self.PageStack.addWidget(self.main_page) # Index 0
        self.PageStack.addWidget(self.home_page) # Index 1

        self.setCentralWidget(self.PageStack)
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()
