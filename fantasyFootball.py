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
DRAFT = 6

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
# 6 - DraftWidget

class MainWindow(QtWidgets.QMainWindow):  # Main Window
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setup()

    def setup(self):
        self.setGeometry(0, 0, 700, 700)
        self.setFixedSize(700, 700)  # eliminating resizing
        self.setWindowTitle("Hardcore Fantasy Football")
        #self.setStyleSheet("QMainWindow {background: '#009900';}");
        #self.setStyleSheet("QMainWindow {background-image: url(background.png);}");
        self.setStyleSheet("QMainWindow {background-image: url(matchBackground.jpeg);}");


        #Title Font
        self.fontTitle = QFont()
        self.fontTitle.setBold(True)
        self.fontTitle.setPointSize(35)

        self.titleLabel = QtWidgets.QLabel(self)
        #self.titleLabel.setText("Hardcore\nFantasy\nFootball")
        self.titleLabel.resize(590, 150)
        self.titleLabel.move(260, 75)
        self.titleLabel.setFont(self.fontTitle)
        self.titleLabel.setStyleSheet("QLabel {color: '#ffff00';}");

        self.PageStack = QStackedWidget(self)

        # Creating our pages for the stack
        self.main_page = LoginRegisterWidget(self)
        self.home_page = HomeWidget(self)
        self.register_page = RegisterWidget(self)
        self.login_page = LoginWidget(self)
        self.create_page = CreateWidget(self)
        self.match_page = MatchWidget(self)
        self.draft_page = DraftWidget(self)

        # Adding to stack; Pages indexed in order of addition
        self.PageStack.addWidget(self.main_page) # Index 0
        self.PageStack.addWidget(self.home_page) # Index 1
        self.PageStack.addWidget(self.register_page) # Index 2
        self.PageStack.addWidget(self.login_page) # Index 3
        self.PageStack.addWidget(self.create_page) # Index 4
        self.PageStack.addWidget(self.match_page) # Index 5
        self.PageStack.addWidget(self.draft_page) # Index 6

        self.setCentralWidget(self.PageStack)
        self.show()


# To change between Pages - self.parent().setCurrentIndex(HOME)
#          Changes depending on what you want to switch to ^
class LoginRegisterWidget(QtWidgets.QWidget):  # Normal LoginPage
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        #MainWindow.__init__(self)
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
        self.loginUserTextbox.setPlaceholderText("Enter Username")

        self.loginPassTextbox = QtWidgets.QLineEdit(self)
        self.loginPassTextbox.setFixedSize(280, 40)
        self.loginPassTextbox.setPlaceholderText("Enter Password")

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
        print(self.Login_Username)

        # By passing database checking REMEMBER TO REMOVE
        #self.parent().setCurrentIndex(HOME)
        
        if self.Login_Username != "" and self.Login_Password != "":
            self.loginUsrPassDict = {'username': self.Login_Username, 'password': self.Login_Password}
            headers = {'Content-type': 'application/json'}
            r = s.post(url = url1, headers=headers, data=json.dumps(self.loginUsrPassDict))
            print(r.text)
            if r.text == "success":
                self.parent().setCurrentIndex(HOME)
            else:
                self.login_error = QMessageBox()
                self.login_error.resize(50,50)
                self.login_error.move(80,320)
                self.login_error.setWindowTitle("Error")
                self.login_error.setText("Incorrect\nUsername/Password")
                self.login_error.show()

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
        self.regUserTextbox.setPlaceholderText("Create Username")

        self.regPassTextbox = QLineEdit(self)
        self.regPassTextbox.setFixedSize(280, 40)
        self.regPassTextbox.setPlaceholderText("Create Password")

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
        
        #error box for if user already exists
        if r.text == "error":
            self.regError = QMessageBox()
            self.regError.resize(50,50)
            self.regError.move(80,320)
            self.regError.setWindowTitle("Error")
            self.regError.setText("User Already Exists")
            self.regError.show()

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
                self.matchJoined = QMessageBox()
                self.matchJoined.resize(50,50)
                self.matchJoined.move(80,320)
                self.matchJoined.setWindowTitle("Success")
                self.matchJoined.setText("Match Joined!")
                self.matchJoined.show()
                self.parent().setCurrentIndex(HOME)



        self.matchlist = MatchList()
        self.matchlist.show()

    def current_click(self):
        #if draft is NOT complete:
        self.parent().setCurrentIndex(DRAFT)
        #if draft is complete:
        #self.parent().setCurrentIndex(MATCH)

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
        s.get(url='http://162.243.35.210:5000/exit')
        self.logout_success = QMessageBox()
        self.logout_success.resize(50,50)
        self.logout_success.move(80,320)
        self.logout_success.setWindowTitle("Success")
        self.logout_success.setText("Logout Succesful")
        self.logout_success.show()
        self.parent().setCurrentIndex(LOGIN_REGISTER)
        

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
        self.createMatchTextbox.setPlaceholderText("Create New Match Title")


        # Create a button in the window
        self.createMatchBtn = QPushButton('Create Match', self)
        self.createMatchBtn.setFixedSize(280, 40)
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
            self.matchCreated = QMessageBox()
            self.matchCreated.resize(50,50)
            self.matchCreated.move(80,320)
            self.matchCreated.setWindowTitle("Success")
            self.matchCreated.setText("Match Created!")
            self.matchCreated.show()
            self.parent().setCurrentIndex(HOME)


        
        self.createMatchTextbox.setText("")
        self.Create_Match_Title = ""

    def back_click(self):
        self.parent().setCurrentIndex(HOME)

class DraftWidget(QtWidgets.QWidget):  # DraftWidget for drafting
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.draft()

    def draft(self):
        # Our Layout
        self.box_layout = QtWidgets.QVBoxLayout()
        self.box_layout.setAlignment(Qt.AlignCenter)

        self.draftPlayerTextbox = QLineEdit(self)
        self.draftPlayerTextbox.setFixedSize(280,40)
        self.draftPlayerTextbox.setPlaceholderText("Search Player By Last Name")

        # Search player button
        self.draftPlayerBtn = QPushButton('Search Player', self)
        self.draftPlayerBtn.setFixedSize(280, 40)
        self.draftPlayerBtn.clicked.connect(self.draftPlayer_clicked)

        # Search player button
        self.finishDraftBtn = QPushButton('Complete Draft', self)
        self.finishDraftBtn.setFixedSize(280, 40)
        self.finishDraftBtn.clicked.connect(self.finishDraft_clicked)

        # Back button for create page, back to home page.
        self.backButton = QPushButton('Back', self)
        self.backButton.setFixedSize(280, 40)
        self.backButton.clicked.connect(self.back_clicked)

        # Adding Widgets to Box Layout
        self.box_layout.addWidget(self.draftPlayerTextbox)
        self.box_layout.addWidget(self.draftPlayerBtn)
        self.box_layout.addWidget(self.finishDraftBtn)
        self.box_layout.addWidget(self.backButton)
        
        self.setLayout(self.box_layout)
        self.show()
 
    def draftPlayer_clicked(self):
        self.draftedPlayer = self.draftPlayerTextbox.text()
        
        if self.draftedPlayer!="":
            self.lastName = {'player' : self.draftedPlayer}
            headers = {'Content-type' : 'application/json'}
            r = s.post(url = 'http://162.243.35.210:5000/getlistplayers', headers=headers, data=json.dumps(self.lastName))
            print(r.text)
            #self.parent().setCurrentIndex(MATCH)
        
        self.draftPlayerTextbox.setText("")

        # if self.draftedPlayer != ""
        class PlayerList(QListWidget):
            def __init__(self):
                QListWidget.__init__(self)
                self.add_players()
                self.itemClicked.connect(self.player_click)

            def add_players(self):  # Show list of players containing searched last name 
                for player_text in r.text.split():
                    player = QListWidgetItem(player_text)
                    self.addItem(player)

            def player_click(self, player):
                # Will add a player to their team's database checking their and other teams database for that player's name
                self.playerDict = {'player' : (str(player.text()))}
                headers = {'Content-type' : 'application/json'}
                r = s.post(url = 'http://162.243.35.210:5000/addplayer', headers=headers, data=json.dumps(self.playerDict))

        self.player_list = PlayerList()
        self.player_list.show()


    def finishDraft_clicked(self):
        #REMOVE
        #self.parent().setCurrentIndex(MATCH)


        self.isRosterFull = s.get(url= 'http://162.243.35.210:5000/isrosterfull')
        self.plyrsCmpltdDraft = s.get(url= 'http://162.243.35.210:5000/isdraftover')
        self.plyrsCmpltdDraft = int(self.plyrsCmpltdDraft.text)
        print(self.isRosterFull.text)

        if self.isRosterFull.text != "true":
            self.rosterFull_error = QMessageBox()
            self.rosterFull_error.resize(50,50)
            self.rosterFull_error.move(80,320)
            self.rosterFull_error.setWindowTitle("Error")
            self.rosterFull_error.setText("Roster Is Not Full")
            self.rosterFull_error.show()
            
        if self.plyrsCmpltdDraft == 1:
            self.oneCmpltdDraft = QMessageBox()
            self.oneCmpltdDraft.resize(50,50)
            self.oneCmpltdDraft.move(80,320)
            self.oneCmpltdDraft.setWindowTitle("Success")
            self.oneCmpltdDraft.setText("P1 Picks Are In!\nNext Player's Turn!")
            self.oneCmpltdDraft.show()
        elif self.plyrsCmpltdDraft == 2:
            self.twoCmpltdDraft = QMessageBox()
            self.twoCmpltdDraft.resize(50,50)
            self.twoCmpltdDraft.move(80,320)
            self.twoCmpltdDraft.setWindowTitle("Success")
            self.twoCmpltdDraft.setText("P2 Picks Are In!\nDraft Complete!")
            self.twoCmpltdDraft.show()
            self.parent().setCurrentIndex(MATCH)
        elif self.plyrsCmpltdDraft > 2:
            #REMOVE
            self.parent().setCurrentIndex(MATCH)

    def back_clicked(self):
        self.parent().setCurrentIndex(HOME)

class MatchWidget(QtWidgets.QWidget):  # CreateWidget for creating match
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)

        #Return Home Button
        self.goHome_button = QtWidgets.QPushButton("Go Home", self)
        self.goHome_button.setFixedSize(75, 40)
        self.goHome_button.move(620, 5)
        self.goHome_button.clicked.connect(self.goHome_clicked)

        #Match Label
        self.fontMatch = QFont()
        self.fontMatch.setBold(True)
        self.fontMatch.setPointSize(20)

        self.matchLabel = QtWidgets.QLabel(self)
        self.matchLabel.resize(590, 50)
        self.matchLabel.move(30, 0)
        self.matchLabel.setFont(self.fontMatch)
        self.matchLabel.setStyleSheet("QLabel {color: '#ffff00';}");


    #USERNAME LABELS
        self.fontUsers = QFont()
        self.fontUsers.setPointSize(18)

        self.usrlabelP1 = QtWidgets.QLabel(self)
        self.usrlabelP1.resize(320, 25)
        self.usrlabelP1.move(30, 66)
        self.usrlabelP1.setFont(self.fontUsers)
        self.usrlabelP1.setStyleSheet("QLabel {color: '#ffff00';}");


        self.usrlabelP2 = QtWidgets.QLabel(self)
        self.usrlabelP2.resize(320, 25)
        self.usrlabelP2.move(380, 66)
        self.usrlabelP2.setFont(self.fontUsers)
        self.usrlabelP2.setStyleSheet("QLabel {color: '#ffff00';}");

    #SCORELABELS
        self.fontScores = QFont()
        self.fontScores.setBold(True)
        self.fontScores.setPointSize(18)

        self.scorelabelP1 = QtWidgets.QLabel(self)
        self.scorelabelP1.resize(320, 20)
        self.scorelabelP1.move(130, 130)
        self.scorelabelP1.setFont(self.fontScores)
        self.scorelabelP1.setStyleSheet("QLabel {color: '#ffff00';}");

        self.scorelabelP2 = QtWidgets.QLabel(self)
        self.scorelabelP2.resize(320, 20)
        self.scorelabelP2.move(480, 130)
        self.scorelabelP2.setFont(self.fontScores)
        self.scorelabelP2.setStyleSheet("QLabel {color: '#ffff00';}");


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
        self.QBlabelP1.setStyleSheet("QLabel {color: '#ffff00';}");

        self.RBlabelP1 = QtWidgets.QLabel(self)
        self.RBlabelP1.setText("RB")
        self.RBlabelP1.resize(50, 20)
        self.RBlabelP1.move(30, 275)
        self.RBlabelP1.setFont(self.fontPosition)
        self.RBlabelP1.setStyleSheet("QLabel {color: '#ffff00';}");


        self.WRlabelP1 = QtWidgets.QLabel(self)
        self.WRlabelP1.setText("WR")
        self.WRlabelP1.resize(50, 20)
        self.WRlabelP1.move(30, 350)
        self.WRlabelP1.setFont(self.fontPosition)
        self.WRlabelP1.setStyleSheet("QLabel {color: '#ffff00';}");

        self.KlabelP1 = QtWidgets.QLabel(self)
        self.KlabelP1.setText("K")
        self.KlabelP1.resize(50, 20)
        self.KlabelP1.move(30, 425)
        self.KlabelP1.setFont(self.fontPosition)
        self.KlabelP1.setStyleSheet("QLabel {color: '#ffff00';}");


    #p2 position labels
        self.QBlabelP2 = QtWidgets.QLabel(self)
        self.QBlabelP2.setText("QB")
        self.QBlabelP2.resize(50, 20)
        self.QBlabelP2.move(380, 200)
        self.QBlabelP2.setFont(self.fontPosition)
        self.QBlabelP2.setStyleSheet("QLabel {color: '#ffff00';}");

        self.RBlabelP2 = QtWidgets.QLabel(self)
        self.RBlabelP2.setText("RB")
        self.RBlabelP2.resize(50, 20)
        self.RBlabelP2.move(380, 275)
        self.RBlabelP2.setFont(self.fontPosition)
        self.RBlabelP2.setStyleSheet("QLabel {color: '#ffff00';}");

        self.WRlabelP2 = QtWidgets.QLabel(self)
        self.WRlabelP2.setText("WR")
        self.WRlabelP2.resize(50, 20)
        self.WRlabelP2.move(380, 350)
        self.WRlabelP2.setFont(self.fontPosition)
        self.WRlabelP2.setStyleSheet("QLabel {color: '#ffff00';}");

        self.KlabelP2 = QtWidgets.QLabel(self)
        self.KlabelP2.setText("K")
        self.KlabelP2.resize(50, 20)
        self.KlabelP2.move(380, 425)
        self.KlabelP2.setFont(self.fontPosition)
        self.KlabelP2.setStyleSheet("QLabel {color: '#ffff00';}"); 


        #font for player names
        self.fontPlayerName = QFont()
        self.fontPlayerName.setPointSize(16)
        self.fontPlayerName.setBold(True)


    #p1 player names
        self.QBnameP1 = QtWidgets.QLabel(self)
        self.QBnameP1.resize(160, 20)
        self.QBnameP1.move(90, 200)
        self.QBnameP1.setFont(self.fontPlayerName)
        self.QBnameP1.setStyleSheet("QLabel {color: '#ffff00';}");   

        self.RBnameP1 = QtWidgets.QLabel(self)
        self.RBnameP1.resize(160, 20)
        self.RBnameP1.move(90, 275)
        self.RBnameP1.setFont(self.fontPlayerName)
        self.RBnameP1.setStyleSheet("QLabel {color: '#ffff00';}");   

        self.WRnameP1 = QtWidgets.QLabel(self)
        self.WRnameP1.resize(160, 20)
        self.WRnameP1.move(90, 350)
        self.WRnameP1.setFont(self.fontPlayerName)
        self.WRnameP1.setStyleSheet("QLabel {color: '#ffff00';}");   

        self.KnameP1 = QtWidgets.QLabel(self)
        self.KnameP1.resize(160, 20)
        self.KnameP1.move(90, 425)
        self.KnameP1.setFont(self.fontPlayerName)
        self.KnameP1.setStyleSheet("QLabel {color: '#ffff00';}");   



    #p2 player names
        self.QBnameP2 = QtWidgets.QLabel(self)
        self.QBnameP2.resize(160, 20)
        self.QBnameP2.move(440, 200)
        self.QBnameP2.setFont(self.fontPlayerName)
        self.QBnameP2.setStyleSheet("QLabel {color: '#ffff00';}");   

        self.RBnameP2 = QtWidgets.QLabel(self)
        self.RBnameP2.resize(160, 20)
        self.RBnameP2.move(440, 275)
        self.RBnameP2.setFont(self.fontPlayerName)
        self.RBnameP2.setStyleSheet("QLabel {color: '#ffff00';}");   

        self.WRnameP2 = QtWidgets.QLabel(self)
        self.WRnameP2.resize(160, 20)
        self.WRnameP2.move(440, 350)
        self.WRnameP2.setFont(self.fontPlayerName)
        self.WRnameP2.setStyleSheet("QLabel {color: '#ffff00';}");   

        self.KnameP2 = QtWidgets.QLabel(self)
        self.KnameP2.resize(160, 20)
        self.KnameP2.move(440, 425)
        self.KnameP2.setFont(self.fontPlayerName)
        self.KnameP2.setStyleSheet("QLabel {color: '#ffff00';}");   



    #font for player scores
        self.fontPlayerScore = QFont()
        self.fontPlayerScore.setPointSize(14)
        self.fontPlayerScore.setBold(True)

    #p1 player scores
        self.QBscoreP1 = QtWidgets.QLabel(self)
        self.QBscoreP1.resize(90, 20)
        self.QBscoreP1.move(260, 200)
        self.QBscoreP1.setFont(self.fontPlayerScore)
        self.QBscoreP1.setStyleSheet("QLabel {color: '#ffff00';}");   

        self.RBscoreP1 = QtWidgets.QLabel(self)
        self.RBscoreP1.resize(90, 20)
        self.RBscoreP1.move(260, 275)
        self.RBscoreP1.setFont(self.fontPlayerScore)
        self.RBscoreP1.setStyleSheet("QLabel {color: '#ffff00';}");   

        self.WRscoreP1 = QtWidgets.QLabel(self)
        self.WRscoreP1.resize(90, 20)
        self.WRscoreP1.move(260, 350)
        self.WRscoreP1.setFont(self.fontPlayerScore)
        self.WRscoreP1.setStyleSheet("QLabel {color: '#ffff00';}");   

        self.KscoreP1 = QtWidgets.QLabel(self)
        self.KscoreP1.resize(90, 20)
        self.KscoreP1.move(260, 425)
        self.KscoreP1.setFont(self.fontPlayerScore)
        self.KscoreP1.setStyleSheet("QLabel {color: '#ffff00';}");   

    #p2 player scores
        self.QBscoreP2 = QtWidgets.QLabel(self)
        self.QBscoreP2.resize(90, 20)
        self.QBscoreP2.move(610, 200)
        self.QBscoreP2.setFont(self.fontPlayerScore)
        self.QBscoreP2.setStyleSheet("QLabel {color: '#ffff00';}");   

        self.RBscoreP2 = QtWidgets.QLabel(self)
        self.RBscoreP2.resize(90, 20)
        self.RBscoreP2.move(610, 275)
        self.RBscoreP2.setFont(self.fontPlayerScore)
        self.RBscoreP2.setStyleSheet("QLabel {color: '#ffff00';}");   

        self.WRscoreP2 = QtWidgets.QLabel(self)
        self.WRscoreP2.resize(90, 20)
        self.WRscoreP2.move(610, 350)
        self.WRscoreP2.setFont(self.fontPlayerScore)
        self.WRscoreP2.setStyleSheet("QLabel {color: '#ffff00';}");   

        self.KscoreP2 = QtWidgets.QLabel(self)
        self.KscoreP2.resize(90, 20)
        self.KscoreP2.move(610, 425)
        self.KscoreP2.setFont(self.fontPlayerScore)
        self.KscoreP2.setStyleSheet("QLabel {color: '#ffff00';}");   

        #self.matchStats()

    #def showEvent(self, event):
    #def matchStats(self):
    def showEvent(self, event):
        #self.parent().setStyleSheet("QMainWindow {background-image: url(matchBackground.jpeg);}");
        #Necessary
        #self.parent().titleLabel.setText("")
        self.playerStats = s.get(url= 'http://162.243.35.210:5000/getscores')
        self.playerStats = self.playerStats.text.split()
        print(self.playerStats)

    #calculate p1 scores
        #UPDATE ALL PLAYER STATS WITH API (self.statistic = int(string statistic from API))
        self.QBP1passYds=int(self.playerStats[0])
        self.QBP1touchdwns=int(self.playerStats[1])
        self.QBP1score = self.QBP1passYds/20 + self.QBP1touchdwns*6

        self.RBP1rushYds=int(self.playerStats[2])
        self.RBP1touchdwns=int(self.playerStats[3])
        self.RBP1score = self.RBP1rushYds/10 + self.RBP1touchdwns*6

        self.WRP1passYds=int(self.playerStats[4])
        self.WRP1touchdwns=int(self.playerStats[5])
        self.WRP1score = self.WRP1passYds/10 + self.WRP1touchdwns*6

        self.KP1extraPts=int(self.playerStats[6])
        self.KP1fg=int(self.playerStats[7])
        self.KP1score = self.KP1extraPts/1 + self.KP1fg*3

        #find what def statistics are on API
        #self.DEFP1score = 6.0

        self.scoreP1= self.QBP1score + self.RBP1score + self.WRP1score + self.KP1score #+ self.DEFP1score

    #calculate p2 scores

        #UPDATE ALL PLAYER STATS WITH API (self.statistic = int(string statistic from API))
        self.QBP2passYds=int(self.playerStats[8])
        self.QBP2touchdwns=int(self.playerStats[9])

        self.QBP2score = self.QBP2passYds/20 + self.QBP2touchdwns*6

        self.RBP2rushYds=int(self.playerStats[10])
        self.RBP2touchdwns=int(self.playerStats[11])
        self.RBP2score = self.RBP2rushYds/10 + self.RBP2touchdwns*6

        self.WRP2passYds=int(self.playerStats[12])
        self.WRP2touchdwns=int(self.playerStats[13])
        self.WRP2score = self.WRP2passYds/10 + self.WRP2touchdwns*6

        self.KP2extraPts=int(self.playerStats[14])
        self.KP2fg=int(self.playerStats[15])
        self.KP2score = self.KP2extraPts/1 + self.KP2fg*3

        #find what def statistics are on API
        #self.DEFP2score = 4.0

        self.scoreP2= self.QBP2score + self.RBP2score + self.WRP2score + self.KP2score #+ self.DEFP2score

    

        ####

        #RETRIEVE ACTUAL MATCH NAME FROM DATABASE
        self.matchName = s.get(url= 'http://162.243.35.210:5000/getmatch')
        self.matchName = self.matchName.text
        self.matchLabel.setText(self.matchName)

        #RETRIEVE ACTUAL USER 1 NAME FROM DATABASE
        self.user1Name = s.get(url= 'http://162.243.35.210:5000/getplayer1')
        self.user1Name = self.user1Name.text
        self.usrlabelP1.setText(self.user1Name)

        #RETRIEVE ACTUAL USER 2 NAME FROM DATABASE
        self.user2Name = s.get(url= 'http://162.243.35.210:5000/getplayer2')
        self.user2Name = self.user2Name.text
        self.usrlabelP2.setText(self.user2Name)


        #RETRIEVE ACTUAL SCORE P1 NAME FROM DATABASE
        self.scoreP1Str = str(self.scoreP1)
        self.scorelabelP1.setText(self.scoreP1Str)


        #RETRIEVE ACTUAL SCORE P2 NAME FROM DATABASE
        self.scoreP2Str = str(self.scoreP2)
        self.scorelabelP2.setText(self.scoreP2Str)


        self.playerNames = s.get(url= 'http://162.243.35.210:5000/getplayers')
        self.playerNames = self.playerNames.text.split()
        print(self.playerNames)


        #RETRIEVE ACTUAL QB P1 NAME FROM DATABASE
        self.playerNames[0]
        self.QBnameP1.setText(self.playerNames[0])


        #RETRIEVE ACTUAL RB P1 NAME FROM DATABASE
        self.playerNames[1]
        self.RBnameP1.setText(self.playerNames[1])

        #RETRIEVE ACTUAL WR P1 NAME FROM DATABASE
        self.playerNames[2]
        self.WRnameP1.setText(self.playerNames[2])

        #RETRIEVE ACTUAL K P1 NAME FROM DATABASE
        self.playerNames[3]
        self.KnameP1.setText(self.playerNames[3])


        #RETRIEVE ACTUAL QB P2 NAME FROM DATABASE
        self.playerNames[4]
        self.QBnameP2.setText(self.playerNames[4])


        #RETRIEVE ACTUAL RB P2 NAME FROM DATABASE
        self.playerNames[5]
        self.RBnameP2.setText(self.playerNames[5])


        #RETRIEVE ACTUAL WR P2 NAME FROM DATABASE
        self.playerNames[6]
        self.WRnameP2.setText(self.playerNames[6])


        #RETRIEVE ACTUAL K P2 NAME FROM DATABASE
        self.playerNames[7]
        self.KnameP2.setText(self.playerNames[7])

        #RETRIEVE ACTUAL QB P1 score FROM DATABASE
        self.QBP1scoreStr = str(self.QBP1score) + " pts"
        self.QBscoreP1.setText(self.QBP1scoreStr)

        #RETRIEVE ACTUAL RB P1 score FROM DATABASE
        self.RBP1scoreStr = str(self.RBP1score) + " pts"
        self.RBscoreP1.setText(self.RBP1scoreStr)

        #RETRIEVE ACTUAL WR P1 score FROM DATABASE
        self.WRP1scoreStr = str(self.WRP1score) + " pts"
        self.WRscoreP1.setText(self.WRP1scoreStr)

        #RETRIEVE ACTUAL K P1 score FROM DATABASE
        self.KP1scoreStr = str(self.KP1score) + " pts"
        self.KscoreP1.setText(self.KP1scoreStr)

        #RETRIEVE ACTUAL QB P2 score FROM DATABASE
        self.QBP2scoreStr = str(self.QBP2score) + " pts"
        self.QBscoreP2.setText(self.QBP2scoreStr)

        #RETRIEVE ACTUAL RB P2 score FROM DATABASE
        self.RBP2scoreStr = str(self.RBP2score) + " pts"
        self.RBscoreP2.setText(self.RBP2scoreStr)


        #RETRIEVE ACTUAL WR P2 score FROM DATABASE
        self.WRP2scoreStr = str(self.WRP2score) + " pts"
        self.WRscoreP2.setText(self.WRP2scoreStr)

        #RETRIEVE ACTUAL K P2 score FROM DATABASE
        self.KP2scoreStr = str(self.KP2score) + " pts"
        self.KscoreP2.setText(self.KP2scoreStr)
        ########


    def goHome_clicked(self):
        self.parent().setCurrentIndex(HOME)

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