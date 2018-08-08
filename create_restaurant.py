from db_schema import *
from mongoengine import *
import os
from random import uniform
user       = os.environ['DB_USER']
password   = os.environ['DB_PASS']
uri = f'mongodb://{user}:{password}@ds153851.mlab.com:53851/gorditos'

#Database connection
connect(db='gorditos',
        username=user,
        password=password,
        host=uri)

#GDL BOUNDARY
#20.742335, -103.461074
#20.551303, -103.221499


for i in range(0,0):
    lat = round(uniform(20.551303,20.742335),6)
    lon = round(uniform(-103.461074,-103.221499),6)
    restaurant = Restaurant(
        name=str(hash(chr(i))),
        location=[lon,lat],
        city='GDL'
    ).save()
#restaurant.save()
result = Restaurant.objects(location__geo_within_sphere=[[-103.391922, 20.673566], 3/6371.0])

for r in result:
    print(r['location'])