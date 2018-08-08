from db_schema import *
from mongoengine import *
from random import uniform

from connect_db import *

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