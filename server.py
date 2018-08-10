import os

from flask import Flask, jsonify, make_response, request, render_template, Response

from functools import wraps

from database_functions import *

import json

from flask_cors import CORS

#SECURITY STUFF
import bcrypt
from hashlib import md5
from random import randint

import settings
#Import predifined schema
from db_schema import Order, Restaurant, User, Session, connect, ObjectIdField

from connect_db import * 

#Flask stuff
app = Flask(__name__)
CORS(app)
app.config['MONGODB_SETTINGS'] = {'db':'gorditos', 'alias':'default'}


#Redirect string
redirect = '<meta http-equiv="refresh" content="0; url=/" />'

#Cookie validation
def valid_session(cookies={}):
    if cookies == {} or 'session' not in cookies:
        return False
    try:
        session = Session.objects.get(session_hash=cookies['session'])
    except Exception as e:
        return False
    return True

def cookie_decorator(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if not valid_session(request.cookies):
            return render_template('login.html')
        return route_function(*args, **kwargs)
    return wrapper


#Hash for cookie
#Note: Sending the ObjectID as a cookie is not safe at all
def random_md5():
    randomString = "".join([
        chr(randint(65,90)) for _ in range(64)
    ])
    md5_hash = md5(randomString.encode()).hexdigest()
    return md5_hash
    

def make_error(message):
    "This method returns a response with error"
    res = {}
    res['status'] = "ERROR"
    res['message'] = message
    return make_response(jsonify(res),401)

@app.route('/users', methods=['GET','POST'])
def users():
    user = User(**request.json)
    try:
        user.save()
    except Exception as e:
        return f"ERROR: MISSING USER PROPERTY\n{e}"

    return 'OK'

@app.route('/login', methods=['POST'])
def login():
    req       = request.json
    res       = {}
    if (req == None): req = request.form
    mail      = req.get('mail')
    password  = req.get('password',"").encode('utf-8')
    try:
        user = User.objects.get(mail=mail)
    except Exception as e:
        print(e)
        return make_error('USER NOT FOUND')

    
    #Check if password matches hashed password
    if bcrypt.checkpw(password, user.hash_password.encode('utf-8')):
        #Create a new session for the user
        session = Session(userID=str(user["id"]), session_hash=random_md5())
        session.save()
        #res.set_cookie('session', str(session["session_hash"]),expires=session.expires_at)
        res["token"] = str(session["session_hash"])
        res["status"]= "OK"
        res = jsonify(res)
        return make_response(res)
    else:
        print("Invalid pass")
        return make_error("WRONG PASSWORD")

    return make_error("UNKNOWN")

@app.route('/register', methods=['POST'])
def register():
    res = {}
    data     = request.json
    if (data == None): data = request.form.to_dict()
    exists   = False

    #Check if the user is already registered
    try:
        user   = User.objects.get(mail=data['mail'])
        exists = True
        print(user['complete'])
        if (user['complete']):
            return make_error("USER ALREADY EXISTS")
    except Exception as e: 
        '''
            User was not found but its okay since this is registration
        '''
        print(e)

    #Create password hash
    hash_password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())

    del data['password']
    data['hash_password'] = hash_password.decode()

    if (exists):
        '''
            If the user already exists in database but the registration is not complete
        '''
        user.update(**data)
        #Create a new session for the user
        session = Session(userID=str(user["id"]), session_hash=random_md5())
        session.save()
        #res.set_cookie('session', str(session["session_hash"]),expires=session.expires_at)
        res["token"]  = str(session["session_hash"])
        res["status"] = "OK"
        res["message"]= "USER UPDATED"
        res = jsonify(res)
        return make_response(res)
    else:
        print("HERE")
        user = User(**data)
        user.save()
        #Create a new session for the user
        session = Session(userID=str(user["id"]), session_hash=random_md5())
        session.save()
        #res.set_cookie('session', str(session["session_hash"]),expires=session.expires_at)
        res["token"]  = str(session["session_hash"])
        res["status"] = "OK"
        res["message"]= "USER CREATED"
        res = jsonify(res)
        return make_response(res)
    return make_error('UNKNOWN ERROR')

@app.route('/logout',methods=['DELETE'])
def logout():
    data     = request.json
    res = {}
    if (data == None): data = request.form.to_dict()
    if data == {}:
        data['session'] = request.args.get('session')
    try:
        Session.objects.get(session_hash=data['session']).delete()
        res['status'] = "OK"
        res['message']= "LOGGED OUT"
        res = jsonify(res)
        return make_response(res)
    except:
        return make_error('INVALID SESSION')

@app.route('/test', methods=['GET'])
@cookie_decorator
def test():
    return "WUDDUP"


@app.route('/near_restaurants', methods=['GET'])
#@cookie_decorator
def home():
    data     = request.json
    if (data == None): data = request.form.to_dict()
    print(data)


    session = request.args.get('session','neutral')
    category= request.args.get('category','all')
    #CENTRAAL
    #20.675094, -103.392790
    lat     = float(request.args.get('lat',20.675094)  )
    lon     = float(request.args.get('lon',-103.392790))
    try:
        results = get_restaurants(session,category, 3,lat,lon)
    except Exception as e:
        print(e)
        return make_error("INVALID USER SESSION")

    res = Response(
        results.to_json(),
        mimetype='application/json'
        )
    
    return res

@app.route('/', methods=['GET'])
def root():
    return "GORDITOS-SABROSITOS-API"

@app.route('/set_location', methods=['POST'])
@cookie_decorator
def set_location():
    data     = request.json
    if (data == None): data = request.form.to_dict()
    user = get_user_by_session(request.cookies['session'])
    new_location = [float(data['long']), float(data['lat'])]
    user['current_location'] = new_location
    try:
        user.save()
        return "OK"
    except:
        return "ERROR"

@app.route('/get_location', methods=['GET'])
@cookie_decorator
def get_location():
    user = get_user_by_session(request.cookies['session'])
    location = user['current_location']['coordinates']
    return str(location)