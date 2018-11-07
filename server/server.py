from flask import Flask
from flask import jsonify
from flask import request
from user import db
from user import User

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
	req_data = request.get_json()
	if 'username' in req_data and 'password' in req_data:
		u = User.query.filter_by(username=req_data['username']).first()
		print(u.password)
		print(hash(req_data['password']))
		if u.password == str(hash(req_data['password'])):
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
		except IntegrityError:
			return jsonify({'error' : 'user already exists'})
	return jsonify({'error' : 'wrong request'})

