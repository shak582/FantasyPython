from flask import Flask
from flask import jsonify
from flask import request
from flask import session
#from flask_session import Session
from flask.ext.session import Session
from user import *
import nflgame


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Session(app)
#db.init_app(app)

games = nflgame.games(2017, week=[x for x in range(1, 18)])
players = nflgame.combine_game_stats(games)
allplayers = set([str(x) for x in players])
players = nflgame.combine_game_stats(games)
passing = [x for x in players.passing()]
players = nflgame.combine_game_stats(games)
rushing = [x for x in players.rushing()]
players = nflgame.combine_game_stats(games)
receiver = [x for x in players.receiving()]
players = nflgame.combine_game_stats(games)
kicking = [x for x in players.kicking()]
rushing = set(rushing) - set(passing)


#USER STUFF##########################################
@app.route('/login', methods=['POST'])
def login():
	req_data = request.get_json()
	if 'username' in req_data and 'password' in req_data:
		try:
			u = User.query.filter_by(username=req_data['username']).first()
			if u.password == str(hash(req_data['password'])):
				session['username'] = req_data['username']
				print(session['username'])
				#return jsonify({'success' : 'right shit'})
				return 'success'
		except Exception:
			return 'error'
	#return jsonify({'error' : 'wrong request'})
	return 'error'

@app.route('/register', methods=['POST'])
def register():
	req_data = request.get_json()
	if 'username' in req_data and 'password' in req_data:
		try:
			if User.query.filter_by(username=req_data['username']).first() != None:
				return 'error'
			u = User()
			u.username = req_data['username']
			u.password = hash(req_data['password'])
			db.session.add(u)
			db.session.commit()
			session['username'] = req_data['username']
			#return jsonify({'success' : 'right shit'})
			return 'success'
		except Exception:
			#return jsonify({'error' : 'user already exists'})
			return 'error'
	#return jsonify({'error' : 'wrong request'})
	return 'error'


@app.route('/getusername', methods=['GET'])
def getusername():
	return session['username']

@app.route('/exit', methods=['GET'])
def exits():
	if 'username' in session:
		del session['username']
	return 'success'

#MATCH STUFF################################################
@app.route('/creatematch', methods=['POST'])
def createMatch():
	req_data = request.get_json()
	print req_data
	if 'username' in session and 'match' in req_data:
		try:
			m = Match()
			m.match = req_data['match']
			m.player1 = session['username']
			m.state = 'draft'
			db.session.add(m)
			db.session.commit()
			for x in players:
				t = Player()
				t.name = str(x)
				t.name = t.match
				t.valid = False
				db.session.add(t)
				db.session.commit()
			return jsonify({'success' : 'right shit'})
		except Exception as e:
			return jsonify({'error':e.args})
	return jsonify({'error' : 'wrong request or not logged in'})

@app.route('/joinmatch', methods=['POST'])
def joinMatch():
	req_data = request.get_json()
	if 'username' in session and 'match' in req_data:
		try:
			m = Match.query.filter_by(match=req_data['match']).first()
			print m
			if not m:
				return jsonify({'error' : 'match doesnt exist'})
			if m.player1 == session['username']:
				return jsonify({'error' : 'user is already in match'})
			m.player2 = session['username']
			db.session.commit()
			return 'success'
		except Exception as e:
			return jsonify({'error' : 'match dont exist'})
	return jsonify({'error' : 'good shit'})

@app.route('/getallmatches', methods=['GET'])
def getAllMatches():
	ms = Match.query.all()
	s = ''
	for x in ms:
		if not x.player2:
			s += x.match + '\n'
	return 'none' if s=='' else s

@app.route('/getmymatches', methods=['GET'])
def getMyMatches():
	if 'username' in session:
		try:
			m = set(Match.query.filter_by(player1=session['username']).all())
			d = set(Match.query.filter_by(player2=session['username']).all())

			c = list(m | d)

			s = ''

			for x in c:
				s += x + '\n'

			return s
		except Exception as e:
			return e.args
	return 'not logged in'

@app.route('/getlistplayers', methods=['POST'])
def checkPlayer():
	req_data = request.get_json()
	if 'username' in session and 'match' in req_data and 'player' in req_data:
		ps = list(filter(lambda a: req_data['player'] in a, allplayers))
		return ' '.join(ps)
	return False


# @app.route('/draftplayer', methods=['POST'])
# def draftplayer():
# 	req_data = request.get_json()
# 	if 'match' in req_data and 'player' in req_data:
# 		try:
# 			m = Match.query.filter_by(req_data['match'])
# 			if not m:
# 				return 'error no match like that exists'

# 		except Exception:
# 			return 'error'




app.run()
