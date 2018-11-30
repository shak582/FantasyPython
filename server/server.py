from flask import Flask
from flask import jsonify
from flask import request
from flask import session
from flask.ext.session import Session
from user import db
from user import User


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route('/login', methods=['POST'])
def login():
	req_data = request.get_json()
	if 'username' in req_data and 'password' in req_data:
		u = User.query.filter_by(username=req_data['username']).first()
		if u.password == str(hash(req_data['password'])):
			session['username'] = req_data['username']
			print(session['username'])
			return jsonify({'success' : 'right shit'})
	return jsonify({'error' : 'wrong request'})

@app.route('/register', methods=['POST'])
def register():
	req_data = request.get_json()
	if 'username' in req_data and 'password' in req_data:
		try:
			u = User()
			u.username = req_data['username']
			u.password = hash(req_data['password'])
			db.session.add(u)
			db.session.commit()
			return jsonify({'success' : 'right shit'})
		except Exception:
			return jsonify({'error' : 'user already exists'})
	return jsonify({'error' : 'wrong request'})


@app.route('/getusername', methods=['GET'])
def getusername():
	return session['username']


app.run()
