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
CREATE = 4

url = 'http://shak582.com:5000/register'
url1 = 'http://shak582.com:5000/login'
url3 = 'http://shak582.com:5000/creatematch'
s = requests.session()


# INDEXES FOR STACK
# 0 - LoginRegisterWidget
# 1 - HomeWidget
# 2 - RegisterWidget
# 3 - LoginWidget
# 4 - CreateWidget

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
        self.create_page = CreateWidget(self)

        # Adding to stack; Pages indexed in order of addition
        self.PageStack.addWidget(self.main_page) # Index 0
        self.PageStack.addWidget(self.home_page) # Index 1
        self.PageStack.addWidget(self.register_page) # Index 2
        self.PageStack.addWidget(self.login_page) # Index 3
        self.PageStack.addWidget(self.create_page) # Index 4

        self.setCentralWidget(self.PageStack)
        self.show()


# To change between Pages - self.parent().setCurrentIndex(HOME)
#          Changes depending on what you want to switch to ^
class LoginRegisterWidget(QtWidgets.QWidget):  # Normal LoginPage
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.setup()

    def setup(self):
        # Our Layout
        self.box_layout = QtWidgets.QVBoxLayout()
        self.box_layout.setAlignment(Qt.AlignCenter)
        # Login Button
        self.login_button = QtWidgets.QPushButton("Login", self)
        self.login_button.setFixedSize(280, 40)
        self.login_button.clicked.connect(self.login_click)

        # Register Button
        self.register_button = QtWidgets.QPushButton("Register", self)
        self.register_button.setFixedSize(280, 40)
        self.register_button.clicked.connect(self.register_click)

        # Adding buttons to layout
        self.box_layout.addWidget(self.login_button)
        self.box_layout.addWidget(self.register_button)

        self.setLayout(self.box_layout)

    def register_click(self):
        self.parent().setCurrentIndex(REGISTER)

    def login_click(self):
        self.parent().setCurrentIndex(LOGIN)

class LoginWidget(QtWidgets.QWidget): # Login Widget to login user
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.setup()

    def setup(self):
        # Our Layout
        self.box_layout = QtWidgets.QVBoxLayout()
        self.box_layout.setAlignment(Qt.AlignCenter)

        self.loginUserTextbox = QtWidgets.QLineEdit(self)
        self.loginUserTextbox.setFixedSize(280, 40)

        self.loginPassTextbox = QtWidgets.QLineEdit(self)
        self.loginPassTextbox.setFixedSize(280, 40)

        self.loginBtn = QtWidgets.QPushButton('Login', self)
        self.loginBtn.setFixedSize(280, 40)

        # Back Button
        self.logout_button = QtWidgets.QPushButton("Back", self)
        self.logout_button.clicked.connect(self.login_back_click)

        self.box_layout.addWidget(self.loginUserTextbox)
        self.box_layout.addWidget(self.loginPassTextbox)
        self.box_layout.addWidget(self.loginBtn)



 
        # connect button to function on_click
        self.loginBtn.clicked.connect(self.login_click)
        self.setLayout(self.box_layout)
        self.show()

    def login_back_click(self):
        self.parent().setCurrentIndex(LOGIN_REGISTER)

 
    def login_click(self):
        self.Login_Username = self.loginUserTextbox.text()
        self.Login_Password = self.loginPassTextbox.text()

        # By passing database checking REMEMBER TO 
        # self.parent().setCurrentIndex(HOME)
        
        if self.Login_Username != "" and self.Login_Password != "":
            self.loginUsrPassDict = {'username': self.Login_Username, 'password': self.Login_Password}
            headers = {'Content-type': 'application/json'}
            r = s.post(url = url1, headers=headers, data=json.dumps(self.loginUsrPassDict))
            print(r.text)
            if r.text == "success":
                self.parent().setCurrentIndex(HOME)
        self.loginUserTextbox.setText("")
        self.loginPassTextbox.setText("")


class RegisterWidget(QtWidgets.QWidget): # RegisterWidget for registering user
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.setup()

    def setup(self):
        # Our Layout
        self.box_layout = QtWidgets.QVBoxLayout()
        self.box_layout.setAlignment(Qt.AlignCenter)

        self.regUserTextbox = QLineEdit(self)
        self.regUserTextbox.setFixedSize(280, 40)

        self.regPassTextbox = QLineEdit(self)
        self.regPassTextbox.setFixedSize(280, 40)
        # Create a button in the window
        self.registerBtn = QPushButton('Register', self)
        self.registerBtn.setFixedSize(280, 40)
        # connect button to function on_click
        self.registerBtn.clicked.connect(self.register_click)

        # Adding widgets to layour
        self.box_layout.addWidget(self.regUserTextbox)
        self.box_layout.addWidget(self.regPassTextbox)
        self.box_layout.addWidget(self.registerBtn)

        self.setLayout(self.box_layout)
        self.show()
 
    def register_click(self):
        self.Register_Username = self.regUserTextbox.text()
        self.Register_Password = self.regPassTextbox.text()

        # By passing database checking REMEBER TO REMOVE
        #self.parent().setCurrentIndex(LOGIN_REGISTER)
        
        if self.Register_Username!=None and self.Register_Password !=None:
            self.regUsrPassDict = {'username' : self.Register_Username, 'password' : self.Register_Password}
            headers = {'Content-type' : 'application/json'}
            r = s.post(url = url, headers=headers, data=json.dumps(self.regUsrPassDict))
            print(r.text)
            self.parent().setCurrentIndex(HOME)
        
        self.regUserTextbox=""
        self.regPassTextbox=""



class HomeWidget(QtWidgets.QWidget): # HomeWidget for joining, creating match
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.setup()

    def setup(self):
        # Our Layout
        self.box_layout = QtWidgets.QVBoxLayout()
        self.box_layout.setAlignment(Qt.AlignCenter)
        # Create Match Button
        self.create_button = QtWidgets.QPushButton("Create Match", self)
        self.create_button.setFixedSize(280, 40)
        self.create_button.clicked.connect(self.create_click)

        # Join Match Button
        self.join_button = QtWidgets.QPushButton("Join Match", self)
        self.join_button.setFixedSize(280, 40)
        self.join_button.clicked.connect(self.join_click)

        # Current Match Button
        self.current_button = QtWidgets.QPushButton("Current Match", self)
        self.current_button.setFixedSize(280, 40)
        self.current_button.clicked.connect(self.current_click)

        # Logout Button
        self.logout_button = QtWidgets.QPushButton("Logout", self)
        self.logout_button.clicked.connect(self.logout_click)

        # Adding buttons to layout
        self.box_layout.addWidget(self.create_button)
        self.box_layout.addWidget(self.join_button)
        self.box_layout.addWidget(self.current_button)

        self.setLayout(self.box_layout)

    def create_click(self):
        self.parent().setCurrentIndex(CREATE)

    def join_click(self):
        class MatchList(QListWidget):
            def __init__(self):
                QListWidget.__init__(self)
                self.add_matches()
                self.itemClicked.connect(self.match_click)

            def add_matches(self):
                self.match_text_list = s.get(url= 'http://shak582.com:5000/getallmatches')
                for match_text in self.match_text_list.text.split('\n'):
                    match = QListWidgetItem(match_text)
                    self.addItem(match)

            def match_click(self, match):
                print (str(match.text()))

        self.matchlist = MatchList()
        self.matchlist.show()

    def current_click(self):
        self.garbage = 0
        
    def logout_click(self):
        self.parent().setCurrentIndex(LOGIN_REGISTER)
        s.get(url='http://shak582.com:5000/exit')
        

class CreateWidget(QtWidgets.QWidget):  # CreateWidget for creating match
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.setup()

    def setup(self):
        # Our Layout
        self.box_layout = QtWidgets.QVBoxLayout()
        self.box_layout.setAlignment(Qt.AlignCenter)

        self.createMatchTextbox = QLineEdit(self)
        self.createMatchTextbox.setFixedSize(280,40)


        # Create a button in the window
        self.createMatchBtn = QPushButton('Create Match', self)
        self.createMatchBtn.setFixedSize(280, 40)
        # connect button to function on_click
        self.createMatchBtn.clicked.connect(self.create_click)

        self.BackButton = QPushButton('Back', self)
        self.BackButton.clicked.connect(self.back_click)

        # Adding Widgets to Box Layout
        self.box_layout.addWidget(self.createMatchTextbox)
        self.box_layout.addWidget(self.createMatchBtn)
        
        self.setLayout(self.box_layout)
        self.show()
 
    def create_click(self):
        self.Create_Match_Title = self.createMatchTextbox.text()

        # By passing database checking REMEMBER TO REMOVE
        #self.parent().setCurrentIndex(HOME)
        
        if self.Create_Match_Title!="":
            self.matchTitle = {'match' : self.Create_Match_Title}
            headers = {'Content-type' : 'application/json'}
            r = s.post(url = url3, headers=headers, data=json.dumps(self.matchTitle))
            print(r.text)
            self.parent().setCurrentIndex(HOME)
        
        self.Create_Match_Title = ""

    def back_click(self):
        self.parent().setCurrentIndex(HOME)




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()
