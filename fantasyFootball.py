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
MATCH = 5

url = 'http://162.243.35.210:5000/register'
url1 = 'http://162.243.35.210:5000/login'
url3 = 'http://162.243.35.210:5000/creatematch'
s = requests.session()

# INDEXES FOR STACK
# 0 - LoginRegisterWidget
# 1 - HomeWidget
# 2 - RegisterWidget
# 3 - LoginWidget
# 4 - CreateWidget
# 5 - MatchWidget

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
        self.match_page = MatchWidget(self)

        # Adding to stack; Pages indexed in order of addition
        self.PageStack.addWidget(self.main_page) # Index 0
        self.PageStack.addWidget(self.home_page) # Index 1
        self.PageStack.addWidget(self.register_page) # Index 2
        self.PageStack.addWidget(self.login_page) # Index 3
        self.PageStack.addWidget(self.create_page) # Index 4
        self.PageStack.addWidget(self.match_page) # Index 5

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
        self.loginBtn.clicked.connect(self.login_click)

        # Back Button
        self.logout_button = QtWidgets.QPushButton("Back", self)
        self.logout_button.setFixedSize(280, 40)
        self.logout_button.clicked.connect(self.login_back_click)

        self.box_layout.addWidget(self.loginUserTextbox)
        self.box_layout.addWidget(self.loginPassTextbox)
        self.box_layout.addWidget(self.loginBtn)
        self.box_layout.addWidget(self.logout_button)
 
        # connect button to function on_click
        self.loginBtn.clicked.connect(self.login_click)
        self.setLayout(self.box_layout)
        self.show()

    def login_back_click(self):
        self.parent().setCurrentIndex(LOGIN_REGISTER)

 
    def login_click(self):
        self.Login_Username = self.loginUserTextbox.text()
        self.Login_Password = self.loginPassTextbox.text()

        # By passing database checking REMEMBER TO REMOVE
        #self.parent().setCurrentIndex(HOME)
        
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

        # Back Button
        self.logout_button = QtWidgets.QPushButton("Back", self)
        self.logout_button.clicked.connect(self.register_back_click)

        # connect button to function on_click
        self.registerBtn.clicked.connect(self.register_click)

        # Adding widgets to layour
        self.box_layout.addWidget(self.regUserTextbox)
        self.box_layout.addWidget(self.regPassTextbox)
        self.box_layout.addWidget(self.registerBtn)
        self.box_layout.addWidget(self.logout_button)

        self.setLayout(self.box_layout)
        self.show()

    def register_back_click(self):
        self.parent().setCurrentIndex(LOGIN_REGISTER)

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
            self.parent().setCurrentIndex(LOGIN_REGISTER)
        
        self.regUserTextbox.setText("")
        self.regPassTextbox.setText("")



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
        self.logout_button.setFixedSize(280, 40)

        # Adding buttons to layout
        self.box_layout.addWidget(self.create_button)
        self.box_layout.addWidget(self.join_button)
        self.box_layout.addWidget(self.current_button)
        self.box_layout.addWidget(self.logout_button)

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
                self.match_text_list = s.get(url= 'http://162.243.35.210:5000/getallmatches')
                for match_text in self.match_text_list.text.split('\n'):
                    match = QListWidgetItem(match_text)
                    self.addItem(match)

            def match_click(self, match):
                self.joinMatchDict = {'match' : (str(match.text()))}
                headers = {'Content-type' : 'application/json'}
                r = s.post(url = 'http://162.243.35.210:5000/joinmatch', headers=headers, data=json.dumps(self.joinMatchDict))


        self.matchlist = MatchList()
        self.matchlist.show()

    def current_click(self):
        self.parent().setCurrentIndex(MATCH)
        '''
        class MatchList(QListWidget):
            def __init__(self):
                QListWidget.__init__(self)
                self.add_matches()
                self.itemClicked.connect(self.match_click)

            def add_matches(self):
                self.match_text_list = s.get(url= 'http://162.243.35.210:5000/getmymatches')
                for match_text in self.match_text_list.text.split('\n'):
                    match = QListWidgetItem(match_text)
                    self.addItem(match)

            def match_click(self, match):
                print (str(match.text()))
            '''
        
    def logout_click(self):
        self.parent().setCurrentIndex(LOGIN_REGISTER)
        s.get(url='http://162.243.35.210:5000/exit')
        

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

        # Back button for create page, back to home page.
        self.backButton = QPushButton('Back', self)
        self.backButton.setFixedSize(280, 40)
        self.backButton.clicked.connect(self.back_click)

        # Adding Widgets to Box Layout
        self.box_layout.addWidget(self.createMatchTextbox)
        self.box_layout.addWidget(self.createMatchBtn)
        self.box_layout.addWidget(self.backButton)
        
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
        
        self.createMatchTextbox.setText("")
        self.Create_Match_Title = ""

    def back_click(self):
        self.parent().setCurrentIndex(HOME)

class MatchWidget(QtWidgets.QWidget):  # CreateWidget for creating match
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.setup()

    def setup(self):
    #Match Label
        self.fontMatch = QFont()
        self.fontMatch.setBold(True)
        self.fontMatch.setPointSize(20)

        self.matchLabel = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL MATCH NAME FROM DATABASE
        #self.matchName = string
        self.matchLabel.setText("PYTHON FANTASY MATCH TITLE")
        self.matchLabel.resize(670, 50)
        self.matchLabel.move(30, 0)
        self.matchLabel.setFont(self.fontMatch)


    #USERNAME LABELS
        self.fontUsers = QFont()
        self.fontUsers.setPointSize(18)

        self.usrlabelP1 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL USER 1 NAME FROM DATABASE
        #self.user1Name = string
        self.usrlabelP1.setText("USER 1")
        self.usrlabelP1.resize(320, 20)
        self.usrlabelP1.move(30, 70)
        self.usrlabelP1.setFont(self.fontUsers)

        self.usrlabelP2 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL USER 2 NAME FROM DATABASE
        #self.user2Name = string
        self.usrlabelP2.setText("USER 2")
        self.usrlabelP2.resize(320, 20)
        self.usrlabelP2.move(380, 70)
        self.usrlabelP2.setFont(self.fontUsers)


    #SCORELABELS
        self.fontScores = QFont()
        self.fontScores.setBold(True)
        self.fontScores.setPointSize(18)

        self.scorelabelP1 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL SCORE P1 NAME FROM DATABASE
        #self.scoreP1 = str(int)
        self.scorelabelP1.setText("134.0")
        self.scorelabelP1.resize(320, 20)
        self.scorelabelP1.move(130, 130)
        self.scorelabelP1.setFont(self.fontScores)

        self.scorelabelP2 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL SCORE P2 NAME FROM DATABASE
        #self.scoreP2 = str(int)
        self.scorelabelP2.setText("113.0")
        self.scorelabelP2.resize(320, 20)
        self.scorelabelP2.move(480, 130)
        self.scorelabelP2.setFont(self.fontScores)


    #font for player positions
        self.fontPosition = QFont()
        self.fontPosition.setBold(True)
        self.fontPosition.setPointSize(14)

    #p1 postition labels
        self.QBlabelP1 = QtWidgets.QLabel(self)
        self.QBlabelP1.setText("QB")
        self.QBlabelP1.resize(50, 20)
        self.QBlabelP1.move(30, 200)
        self.QBlabelP1.setFont(self.fontPosition)

        self.RBlabelP1 = QtWidgets.QLabel(self)
        self.RBlabelP1.setText("RB")
        self.RBlabelP1.resize(50, 20)
        self.RBlabelP1.move(30, 275)
        self.RBlabelP1.setFont(self.fontPosition)

        self.WRlabelP1 = QtWidgets.QLabel(self)
        self.WRlabelP1.setText("WR")
        self.WRlabelP1.resize(50, 20)
        self.WRlabelP1.move(30, 350)
        self.WRlabelP1.setFont(self.fontPosition)

        self.KlabelP1 = QtWidgets.QLabel(self)
        self.KlabelP1.setText("K")
        self.KlabelP1.resize(50, 20)
        self.KlabelP1.move(30, 425)
        self.KlabelP1.setFont(self.fontPosition)

        self.DEFlabelP1 = QtWidgets.QLabel(self)
        self.DEFlabelP1.setText("DEF")
        self.DEFlabelP1.resize(50, 20)
        self.DEFlabelP1.move(30, 500)
        self.DEFlabelP1.setFont(self.fontPosition)


    #p2 position labels
        self.QBlabelP2 = QtWidgets.QLabel(self)
        self.QBlabelP2.setText("QB")
        self.QBlabelP2.resize(50, 20)
        self.QBlabelP2.move(380, 200)
        self.QBlabelP2.setFont(self.fontPosition)

        self.RBlabelP2 = QtWidgets.QLabel(self)
        self.RBlabelP2.setText("RB")
        self.RBlabelP2.resize(50, 20)
        self.RBlabelP2.move(380, 275)
        self.RBlabelP2.setFont(self.fontPosition)

        self.WRlabelP2 = QtWidgets.QLabel(self)
        self.WRlabelP2.setText("WR")
        self.WRlabelP2.resize(50, 20)
        self.WRlabelP2.move(380, 350)
        self.WRlabelP2.setFont(self.fontPosition)

        self.KlabelP2 = QtWidgets.QLabel(self)
        self.KlabelP2.setText("K")
        self.KlabelP2.resize(50, 20)
        self.KlabelP2.move(380, 425)
        self.KlabelP2.setFont(self.fontPosition)

        self.DEFlabelP2 = QtWidgets.QLabel(self)
        self.DEFlabelP2.setText("DEF")
        self.DEFlabelP2.resize(50, 20)
        self.DEFlabelP2.move(380, 500)
        self.DEFlabelP2.setFont(self.fontPosition)


    #font for player names
        self.fontPlayerName = QFont()
        self.fontPlayerName.setPointSize(11)

    #p1 player names
        self.QBnameP1 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL QB P1 NAME FROM DATABASE
        #self.QBP1 = string
        self.QBnameP1.setText("T. Brady")
        self.QBnameP1.resize(210, 20)
        self.QBnameP1.move(90, 200)
        self.QBnameP1.setFont(self.fontPlayerName)

        self.RBnameP1 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL RB P1 NAME FROM DATABASE
        #self.RBP1 = string
        self.RBnameP1.setText("K. Drake")
        self.RBnameP1.resize(210, 20)
        self.RBnameP1.move(90, 275)
        self.RBnameP1.setFont(self.fontPlayerName)

        self.WRnameP1 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL WR P1 NAME FROM DATABASE
        #self.WRP1 = string
        self.WRnameP1.setText("B. Cooks")
        self.WRnameP1.resize(210, 20)
        self.WRnameP1.move(90, 350)
        self.WRnameP1.setFont(self.fontPlayerName)

        self.KnameP1 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL K P1 NAME FROM DATABASE
        #self.KP1 = string
        self.KnameP1.setText("A. Vinatieri")
        self.KnameP1.resize(210, 20)
        self.KnameP1.move(90, 425)
        self.KnameP1.setFont(self.fontPlayerName)

        self.DEFnameP1 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL DEF P1 NAME FROM DATABASE
        #self.DEFP1 = string
        self.DEFnameP1.setText("Dolphins")
        self.DEFnameP1.resize(210, 20)
        self.DEFnameP1.move(90, 500)
        self.DEFnameP1.setFont(self.fontPlayerName)


    #p2 player names
        self.QBnameP2 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL QB P2 NAME FROM DATABASE
        #self.QBP2 = string
        self.QBnameP2.setText("P. Mahomes")
        self.QBnameP2.resize(210, 20)
        self.QBnameP2.move(440, 200)
        self.QBnameP2.setFont(self.fontPlayerName)

        self.RBnameP2 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL RB P2 NAME FROM DATABASE
        #self.RBP2 = string
        self.RBnameP2.setText("S. Barkley")
        self.RBnameP2.resize(210, 20)
        self.RBnameP2.move(440, 275)
        self.RBnameP2.setFont(self.fontPlayerName)

        self.WRnameP2 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL WR P2 NAME FROM DATABASE
        #self.WRP2 = string
        self.WRnameP2.setText("O. Beckham")
        self.WRnameP2.resize(210, 20)
        self.WRnameP2.move(440, 350)
        self.WRnameP2.setFont(self.fontPlayerName)

        self.KnameP2 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL K P2 NAME FROM DATABASE
        #self.KP2 = string
        self.KnameP2.setText("J. Tucker")
        self.KnameP2.resize(210, 20)
        self.KnameP2.move(440, 425)
        self.KnameP2.setFont(self.fontPlayerName)

        self.DEFnameP2 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL DEF P2 NAME FROM DATABASE
        #self.DEFP2 = string
        self.DEFnameP2.setText("Saints")
        self.DEFnameP2.resize(210, 20)
        self.DEFnameP2.move(440, 500)
        self.DEFnameP2.setFont(self.fontPlayerName)


    #font for player scores
        self.fontPlayerScore = QFont()
        self.fontPlayerScore.setPointSize(10)

    #p1 player scores
        self.QBscoreP1 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL QB P1 score FROM DATABASE
        #self.QBP1score = str(int) + " pts"
        self.QBscoreP1.setText("19 pts")
        self.QBscoreP1.resize(50, 20)
        self.QBscoreP1.move(300, 200)
        self.QBscoreP1.setFont(self.fontPlayerScore)

        self.RBscoreP1 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL RB P1 score FROM DATABASE
        #self.RBP1score = str(int) + " pts"
        self.RBscoreP1.setText("15 pts")
        self.RBscoreP1.resize(50, 20)
        self.RBscoreP1.move(300, 275)
        self.RBscoreP1.setFont(self.fontPlayerScore)

        self.WRscoreP1 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL WR P1 score FROM DATABASE
        #self.WRP1score = str(int) + " pts"
        self.WRscoreP1.setText("12 pts")
        self.WRscoreP1.resize(50, 20)
        self.WRscoreP1.move(300, 350)
        self.WRscoreP1.setFont(self.fontPlayerScore)

        self.KscoreP1 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL K P1 score FROM DATABASE
        #self.KP1score = str(int) + " pts"
        self.KscoreP1.setText("4 pts")
        self.KscoreP1.resize(50, 20)
        self.KscoreP1.move(300, 425)
        self.KscoreP1.setFont(self.fontPlayerScore)

        self.DEFscoreP1 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL DEF P1 score FROM DATABASE
        #self.DEFP1score = str(int) + " pts"
        self.DEFscoreP1.setText("6 pts")
        self.DEFscoreP1.resize(50, 20)
        self.DEFscoreP1.move(300, 500)
        self.DEFscoreP1.setFont(self.fontPlayerScore)

    #p2 player scores
        self.QBscoreP2 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL QB P2 score FROM DATABASE
        #self.QBP2score = str(int) + " pts"
        self.QBscoreP2.setText("20 pts")
        self.QBscoreP2.resize(50, 20)
        self.QBscoreP2.move(650, 200)
        self.QBscoreP2.setFont(self.fontPlayerScore)

        self.RBscoreP2 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL RB P2 score FROM DATABASE
        #self.RBP2score = str(int) + " pts"
        self.RBscoreP2.setText("11 pts")
        self.RBscoreP2.resize(50, 20)
        self.RBscoreP2.move(650, 275)
        self.RBscoreP2.setFont(self.fontPlayerScore)

        self.WRscoreP2 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL WR P2 score FROM DATABASE
        #self.WRP2score = str(int) + " pts"
        self.WRscoreP2.setText("16 pts")
        self.WRscoreP2.resize(50, 20)
        self.WRscoreP2.move(650, 350)
        self.WRscoreP2.setFont(self.fontPlayerScore)

        self.KscoreP2 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL K P2 score FROM DATABASE
        #self.KP2score = str(int) + " pts"
        self.KscoreP2.setText("3 pts")
        self.KscoreP2.resize(50, 20)
        self.KscoreP2.move(650, 425)
        self.KscoreP2.setFont(self.fontPlayerScore)

        self.DEFscoreP2 = QtWidgets.QLabel(self)
        #RETRIEVE ACTUAL DEF P2 score FROM DATABASE
        #self.DEFP2score = str(int) + " pts"
        self.DEFscoreP2.setText("4 pts")
        self.DEFscoreP2.resize(50, 20)
        self.DEFscoreP2.move(650, 500)
        self.DEFscoreP2.setFont(self.fontPlayerScore)

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        pen = qp.pen()
        pen.setColor(Qt.black)
    #horizontal line 0
        qp.drawLine(10, 50, 690, 50)
    #vertical line
        qp.drawLine(350, 55, 350, 695)
    #horizontal line 1
        qp.drawLine(10, 105, 690, 105)
    #horizontal line 2
        qp.drawLine(10, 175, 690, 175)
    #horizontal line 3
        qp.drawLine(10, 250, 690, 250)
    #horizontal line 4
        qp.drawLine(10, 325, 690, 325)
    #horizontal line 5
        qp.drawLine(10, 400, 690, 400)
    #horizontal line 6
        qp.drawLine(10, 475, 690, 475)

        qp.end()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()