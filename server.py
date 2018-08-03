
import os

from flask import Flask, jsonify, make_response, request



#SECURITY STUFF
import bcrypt

import settings
#Import predifined schema
from db_schema import Order, Restaurant, User, Session, connect

user       = os.environ['DB_USER']
password   = os.environ['DB_PASS']
uri = f'mongodb://{user}:{password}@ds153851.mlab.com:53851/gorditos'

#Database connection
connect(db='gorditos',
        username=user,
        password=password,
        host=uri)

#Flask stuff
app = Flask(__name__)

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
    mail      = req['mail']
    password  = req['password'].encode('utf-8')
    
    try:
        user = User.objects.get(mail=mail)
    except Exception as e:
        res_string =  "User not found"
        return make_response(res_string)
    
    print()

    #Check if password matches hashed password
    if bcrypt.checkpw(password, user.hash_password.encode('utf-8')):
        res = make_response('OK')
        #Create a new session for the user
        session = Session(userID=str(user["id"]))
        session.save()
        res.set_cookie('session', str(session["id"]))
        return res
    else:
        return make_response('Invalid session')
    return make_response("UNKNOWN ERROR")

@app.route('/register', methods=['POST'])
def register():
    data     = request.json
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
    
    hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    del data['password']
    data['hash_password'] = str(hash_password)
    if (exists):
        user.update(**data)
        return "Updated"
    else:
        new_user = User(**data)
        new_user.save()
        return "Created"

    return "Unhandled operation"