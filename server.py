
import os

from flask import Flask, jsonify, make_response, request

import settings
#Import predifined schema
from db_schema import Order, Restaurant, User, connect

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