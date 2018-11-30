import requests
import json

url = 'http://127.0.0.1:5000/login'
url2 = 'http://127.0.0.1:5000/getusername'

s = requests.session()

data = {'username' : 'dude', 'password' : 'lmao'}
headers = {'Content-type': 'application/json',}

r = s.post(url = url, headers = headers,  data = json.dumps(data))
r2 = s.get(url = url2)


print(r.text)
print(r2.text)