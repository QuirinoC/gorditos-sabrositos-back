import os

from flask import Flask, jsonify, make_response, request, render_template, Response

from functools import wraps

from database_functions import *

import json

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
    if (req == None): req = request.form
    mail      = req['mail']
    password  = req['password'].encode('utf-8')
    try:
        user = User.objects.get(mail=mail)
    except Exception:
        res_string =  "User not found"
        print("Invalid user")
        return make_response(res_string)

    
    #Check if password matches hashed password
    if bcrypt.checkpw(password, user.hash_password.encode('utf-8')):
        res = make_response(redirect)
        #Create a new session for the user
        session = Session(userID=str(user["id"]), session_hash=random_md5())
        session.save()
        res.set_cookie('session', str(session["session_hash"]),expires=session.expires_at)
        return res
    else:
        print("Invalid pass")
        return make_response('Invalid mail/password pair')
    print("ERROR")
    return make_response("UNKNOWN ERROR")

@app.route('/register', methods=['POST'])
def register():
    data     = request.json
    if (data == None): data = request.form.to_dict()
    exists   = False
    #Forgive me god for this piece of code
    #Check if the user is already registered
    try:
        user   = User.objects.get(mail=data['mail'])
        exists = True
        if (user.complete):
            return "User already exists"
    except Exception as e: 
        print(e)
    hash_password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())

    del data['password']
    data['hash_password'] = hash_password.decode()

    if (exists):
        user.update(**data)
        res = make_response(redirect)
        #Create a new session for the user
        session = Session(userID=str(user["id"]), session_hash=random_md5())
        session.save()
        res.set_cookie('session', str(session["session_hash"]),expires=session.expires_at)
        return res
    else:
        new_user = User(**data)
        new_user.save()
        return redirect
        #return "Created"
    
    return "Unhandled operation"


@app.route('/test', methods=['GET'])
@cookie_decorator
def test():
    return "WUDDUP"


@app.route('/', methods=['GET'])
@cookie_decorator
def root():
    session = request.cookies['session']

    results = get_restaurants(session, 3)

    res = Response(
        results.to_json(),
        mimetype='application/json'
        )
    
    return res