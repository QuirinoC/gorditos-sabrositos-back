from mongoengine import connect
import os

uri = f'mongodb://{user}:{password}@ds153851.mlab.com:53851/gorditos'
        

#Database connection
try:
        connect(db='gorditos',
                username=user,
                password=password,
                host=uri)
except Exception as e:
        print(e)

#Crash if not connected
