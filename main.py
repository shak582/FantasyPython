import sys
from PyQt5 import QtWidgets, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class LoginRegisterWidget(QtWidgets.QWidget):  # Parent is Homework3 class (Main window)
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.setup()

    def setup(self):
        #Our Layout
        self.box_layout = QtWidgets.QVBoxLayout()
        # Login Button
        self.login_button = QtWidgets.QPushButton("Login", self)
        self.login_button.clicked.connect(self.login_click)

        # Register Button
        self.register_button = QtWidgets.QPushButton("Register", self)
        self.register_button.clicked.connect(self.register_click)

        #Adding buttons to layout
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


class MainWindow(QtWidgets.QMainWindow):  # Main Window
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setup()

    def setup(self):
        self.setGeometry(0, 0, 700, 700)
        self.setFixedSize(700, 700)  # eliminating resizing
        self.PageStack = QStackedWidget(self)
        self.main_page = LoginRegisterWidget(self)
        self.PageStack.addWidget(self.main_page)
        self.setWindowTitle("Fantasy Football")
        self.setCentralWidget(self.PageStack)
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()