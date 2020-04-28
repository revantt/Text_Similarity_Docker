from flask import Flask,jsonify,request
from flask_restful import Api,Resource
from pymongo import MongoClient
import bcrypt
import spacy

app=Flask(__name__)
api=Api(app)

client=MongoClient('mongodb://db:27017')

db=client.similarityDB
users=db.users

def UserExist(uname):
	if users.find({'Username':uname}).count()==0:
		return False
	return True

def VerifyPw(uname,pwd):
	if not UserExist(uname):
		return False

	hashed_pw=users.find({'Username':uname})[0]['Password']

	if bcrypt.hashpw(pwd.encode('utf8'),hashed_pw)==hashed_pw:
		return True
	else:
		return False

def CountTokens(uname):
	return users.find({'Username':uname})[0]['Tokens']

class Register(Resource):
	def post(self):
		data=request.get_json()

		uname=data['username']
		pwd=data['password']

		if (UserExist(uname)):
			retJson={
			"status":301,
			"msg":"Invalid UserName"
			}
			return jsonify(retJson)
		hashed_pw=bcrypt.hashpw(pwd.encode('utf8'),bcrypt.gensalt())

		users.insert({
			'Username':uname,
			'Password':hashed_pw,
			'Tokens':6
			})
		retJson={
		'status':200,
		'msg':'Successfully Signed up'
		}
		return retJson

class Detect(Resource):
	def post(self):
		data=request.get_json()

		uname=data['username']
		pwd=data['password']
		text1=data['text1']
		text2=data['text2']

		if not UserExist(uname):
			retJson={
			'status':301,
			'msg':'You Dont Exist'
			}
			return jsonify(retJson)
		if not VerifyPw(uname,pwd):
			retJson={
			'status':302,
			'msg':'Invalid Password'
			}
			return jsonify(retJson)

		num_tokens=CountTokens(uname)
		if num_tokens<1:
			retJson={
			'status':303,
			'msg':'Out of tokens'
			}
			return jsonify(retJson)
		nlp=spacy.load('en_core_web_sm')

		text1=nlp(text1)
		text2=nlp(text2)

		ratio=text1.similarity(text2)

		retJson={
		'status':200,
		'similarity':ratio,
		'msg':'Successful'
		}

		num_tokens-=1

		users.update({'Username':uname},{'$set':{'Tokens':num_tokens}})

		return jsonify(retJson)

class Refill(Resource):
	def post(self):
		data=request.get_json()
		
		uname=data['username']
		pwd=data['password']

		refill=data['refill']

		if not VerifyPw(uname,pwd):
			retJson={
			'status':301,
			'msg':'Invalid credentials'
			}
			return jsonify(retJson)

		tokens=CountTokens(uname)

		users.update({
			'Username':uname
			},{
			'$set':{
			'Tokens':refill+tokens
			}
			})

		retJson={
		'status':200,
		'msg':'Successfully refilled'
		}
		return retJson

api.add_resource(Register,'/register')
api.add_resource(Detect,'/detect')
api.add_resource(Refill,'/refill')


if __name__ == '__main__':
	app.run(host='0.0.0.0')