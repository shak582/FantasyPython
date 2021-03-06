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
			m.state = 0
			db.session.add(m)
			db.session.commit()
			t = Team()
			t.match = m.match
			t.player = session['username']
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
			t = Team()
			t.match = m.match
			t.player = session['username']
			db.session.add(t)
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
	print(req_data)
	if 'username' in session and 'player' in req_data:
		ps = list(filter(lambda a: req_data['player'] in a, allplayers))
		return ' '.join(ps)
	return 'error'

@app.route('/addplayer', methods=['POST'])
def addPlayer():
	req_data = request.get_json()
	print req_data
	if 'username' in session and 'player' in req_data:
		try:
			ps = req_data['player']
			t = Team.query.filter_by(player=session['username']).first()
			if ps in [str(x) for x in passing]:
				t.QB = ps
			elif ps in [str(x) for x in rushing]:
				t.RB = ps
			elif ps in [str(x) for x in receiver]:
				t.WR = ps 
			elif ps in [str(x) for x in kicking]:
				t.K = ps
			db.session.commit()
			return 'success'
		except Exception:
			return 'success'
	return 'error'


@app.route('/isrosterfull', methods=['GET'])
def isRosterFull():
	if 'username' in session:
		try:
			t = Team.query.filter_by(player=session['username']).first()
			if t.QB == None:
				return 'QBfalse'
			if t.RB == None:
				return 'RBfalse'
			if t.WR == None:
				return 'WRfalse'
			if t.K == None:
				return 'Kfalse'
			m = Match.query.filter_by(match=t.match).first()

			if 	session['username'] == m.player1 and m.state == 0:
				m.state = m.state + 1
			elif session['username'] == m.player2 and m.state == 1:
				m.state = m.state + 1
			db.session.commit()
			if session['username'] == m.player2 and m. state == 0:
				return 'false'
			return 'true'
		except Exception as e:
			return str(e.args)
	return 'flase'

@app.route('/isdraftover', methods=['GET'])
def isDraftOver():
	if 'username' in session:
		try:
			t = Team.query.filter_by(player=session['username']).first()
			m = Match.query.filter_by(match=t.match).first()
			return str(m.state)
		except Exception as e:
			return str(e.args)
	return str(0)

@app.route('/getmatch', methods=['GET'])
def getDraft():
	if 'username' in session:
		try:
			t = Team.query.filter_by(player=session['username']).first()
			m = Match.query.filter_by(match=t.match).first()
			return m.match
		except Exception as e:
			return str(e.args)
	return 'error'


@app.route('/getplayer1', methods=['GET'])
def getP1():
	if 'username' in session:
		try:
			t = Team.query.filter_by(player=session['username']).first()
			m = Match.query.filter_by(match=t.match).first()
			return m.player1
		except Exception as e:
			return str(e.args)
	return 'error'

@app.route('/getplayer2', methods=['GET'])
def getP2():
	if 'username' in session:
		try:
			t = Team.query.filter_by(player=session['username']).first()
			m = Match.query.filter_by(match=t.match).first()
			return m.player2
		except Exception as e:
			return str(e.args)
	return 'error'

@app.route('/getplayers', methods=['GET'])
def getplayers():
	if 'username' in session:
		try:
			t = Team.query.filter_by(player=session['username']).first()
			m = Match.query.filter_by(match=t.match).first()
			t1 = Team.query.filter_by(player=m.player1).first()
			t2 = Team.query.filter_by(player=m.player2).first()
			s = t1.QB + ' ' + t1.RB + ' ' + t1.WR + ' ' + t1.K
			s += ' ' + t2.QB + ' ' + t2.RB + ' ' + t2.WR + ' ' + t2.K
			return s
		except Exception as e:
			return str(e.args)
	return 'error'

@app.route('/getscores', methods=['GET'])
def getScores():
	if 'username' in session:
		try:
			t = Team.query.filter_by(player=session['username']).first()
			m = Match.query.filter_by(match=t.match).first()
			t1 = Team.query.filter_by(player=m.player1).first()
			t2 = Team.query.filter_by(player=m.player2).first()
			scores1 = []
			scores2 = []
			for x in passing:
				if t1.QB == str(x):
					scores1.append(x.passing_yds)
					scores1.append(x.passing_tds)
				if t2.QB == str(x):
					scores2.append(x.passing_yds)
					scores2.append(x.passing_tds)
			for x in rushing:
				if t1.RB == str(x):
					scores1.append(x.rushing_yds)
					scores1.append(x.receiving_tds)
				if t2.RB == str(x):
					scores2.append(x.rushing_yds)
					scores2.append(x.receiving_tds)
			for x in receiver:
				if t1.WR == str(x):
					scores1.append(x.receiving_yds)
					scores1.append(x.receiving_tds)
				if t2.WR == str(x):
					scores2.append(x.receiving_yds)
					scores2.append(x.receiving_tds)
			for x in kicking:
				if t1.K == str(x):
					scores1.append(x.kicking_xpmade)
					scores1.append(x.kicking_fgm)
				if t2.K == str(x):
					scores2.append(x.kicking_xpmade)
					scores2.append(x.kicking_fgm)
			scores1.extend(scores2)
			scores1 = list(map(str, scores1))
			print(scores1)
			return ' '.join(scores1)
		except Exception as e:
			return str(e.args)
	return 'error'


app.run()
