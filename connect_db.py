from mongoengine import connect
import os

is_prod = os.environ.get('IS_HEROKU', None)

if is_prod == 'True':
        uri = f'mongodb://admin:dO5p3rr1@ds153851.mlab.com:53851/gorditos'
        
else:
        user       = os.environ['DB_USER']
        password   = os.environ['DB_PASS']
        uri = f'mongodb://{user}:{password}@ds153851.mlab.com:53851/gorditos'
        

#Database connection
try:
        connect(db='gorditos',
                username=user,
                password=password,
                host=uri)
except:
        pass