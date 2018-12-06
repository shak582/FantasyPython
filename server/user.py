from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(256), nullable=False)


class Match(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	match = db.Column(db.String(80), unique = True, nullable = False)
	player1 = db.Column(db.String(80), db.ForeignKey('user.username'), nullable = False, unique=True)
	player2 = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=True, unique=True)
	state = db.Column(db.String(80), nullable=False)

class Team(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	match = db.Column(db.String(80), db.ForeignKey('match.match'), nullable=False)
	player = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False, unique=True)
	QB = db.Column(db.String(80), unique=False, nullable=True)
	RB = db.Column(db.String(80), unique=False, nullable=True)
	WR = db.Column(db.String(80), unique=False, nullable=True)
	K = db.Column(db.String(80), unique=False, nullable=True)