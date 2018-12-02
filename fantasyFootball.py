import sys
import requests
import json
from PyQt5 import QtWidgets, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

LOGIN_REGISTER = 0
HOME = 1
REGISTER = 2
LOGIN = 3

url = 'http://shak582.com:5000/register'
url1 = 'http://shak582.com:5000/login'
s = requests.session()

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

    def register_click(self):
        self.parent().setCurrentIndex(REGISTER)

    def login_click(self):
        self.parent().setCurrentIndex(LOGIN)

class LoginWidget(QtWidgets.QWidget): # RegisterWidget for registering user
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.setup()

    def setup(self):
        # Our Layout
        self.box_layout = QtWidgets.QVBoxLayout()

        self.loginUserTextbox = QLineEdit(self)
        self.loginUserTextbox.move(20, 20)
        self.loginUserTextbox.resize(280,40)
 

        self.loginPassTextbox = QLineEdit(self)
        self.loginPassTextbox.move(20, 80)
        self.loginPassTextbox.resize(280,40)
        # Create a button in the window
        self.loginBtn = QPushButton('Login', self)
        self.loginBtn.move(20,140)
 
        # connect button to function on_click
        self.loginBtn.clicked.connect(self.on_click)
        self.show()
 
    @pyqtSlot()
    def on_click(self):
        self.Login_Username = self.loginUserTextbox.text()
        self.Login_Password = self.loginPassTextbox.text()

        #By passing database checking REMEBER TO REMOVE
        self.parent().setCurrentIndex(HOME)
        '''
        if self.Login_Username!="" and self.Login_Password !="":
            self.loginUsrPassDict = {'username' : self.Login_Username, 'password' : self.Login_Password}
            headers = {'Content-type' : 'application/json'}
            r = s.post(url = url1, headers=headers, data=json.dumps(self.loginUsrPassDict))
            print(r.text)
            if r.text == "success":
                print ("Succesful")
                self.parent().setCurrentIndex(HOME)
        '''
        self.loginUserTextbox.setText("")
        self.loginPassTextbox.setText("")


class RegisterWidget(QtWidgets.QWidget): # RegisterWidget for registering user
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.setup()

    def setup(self):
        # Our Layout
        self.box_layout = QtWidgets.QVBoxLayout()

        self.regUserTextbox = QLineEdit(self)
        self.regUserTextbox.move(20, 20)
        self.regUserTextbox.resize(280,40)
 

        self.regPassTextbox = QLineEdit(self)
        self.regPassTextbox.move(20, 80)
        self.regPassTextbox.resize(280,40)
        # Create a button in the window
        self.registerBtn = QPushButton('Register', self)
        self.registerBtn.move(20,140)
 
        # connect button to function on_click
        self.registerBtn.clicked.connect(self.on_click)
        self.show()
 
    @pyqtSlot()
    def on_click(self):
        self.Register_Username = self.regUserTextbox.text()
        self.Register_Password = self.regPassTextbox.text()

        #By passing database checking REMEBER TO REMOVE
        self.parent().setCurrentIndex(LOGIN_REGISTER)
        '''
        if self.Register_Username!="" and self.Register_Password !="":
            self.regUsrPassDict = {'username' : self.Register_Username, 'password' : self.Register_Password}
            headers = {'Content-type' : 'application/json'}
            r = s.post(url = url, headers=headers, data=json.dumps(self.regUsrPassDict))
            print(r.text)
            self.parent().setCurrentIndex(HOME)
        '''
        self.regUserTextbox.setText("")
        self.regPassTextbox.setText("")




'''
    def login_click(self):
        self.username = QInputDialog.getText(self, 'Login', 'Enter your username:')
        self.password = QInputDialog.getText(self, 'Login', 'Enter your password:')
        
        if self.username[1] and self.password[1]:
            self.username = self.username[0]
            self.password = self.password[0]
            self.loginUsrPassDict = {'username' : self.username, 'password' : self.password}
            headers = {'Content-type' : 'application/json'}
            r = s.post(url = url1, headers=headers, data=json.dumps(self.loginUsrPassDict))
            print(r.text)
            if r.text == "success":
                print ("Succesful")
                self.parent().setCurrentIndex(HOME)
'''
'''
    def register_click(self):
        self.inputRegUser = QInputDialog.getText(self, 'Register', 'Enter Username')
        self.inputRegPass = QInputDialog.getText(self, 'Register', 'Enter Password')
        
        if self.inputRegUser[1] and self.inputRegPass[1]:
            self.RegUsername = self.inputRegUser[0]
            self.RegPass = self.inputRegPass[0]
            self.regUsrPassDict = {'username' : self.RegUsername, 'password' : self.RegPass}
            headers = {'Content-type' : 'application/json'}
            r = s.post(url = url, headers=headers, data=json.dumps(self.regUsrPassDict))
            print(r.text)
'''


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
        self.inputCreateMatch = QInputDialog.getText(self, 'Match Name', 'Create Match')

    def join_click(self):
        self.inputFindMatch = QInputDialog.getText(self, 'Match Name', 'Find Match')

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
        self.register_page = RegisterWidget(self)
        self.login_page = LoginWidget(self)

        # Adding to stack; Pages indexed in order of addition
        self.PageStack.addWidget(self.main_page) # Index 0
        self.PageStack.addWidget(self.home_page) # Index 1
        self.PageStack.addWidget(self.register_page) # Index 2
        self.PageStack.addWidget(self.login_page) # Index 3

        self.setCentralWidget(self.PageStack)
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()