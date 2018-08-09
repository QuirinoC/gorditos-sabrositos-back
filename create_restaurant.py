from db_schema import *
from mongoengine import *
from random import uniform

from connect_db import *

#GDL BOUNDARY
#20.742335, -103.461074
#20.551303, -103.221499

urls = [
    "https://images.pexels.com/photos/70497/pexels-photo-70497.jpeg?cs=srgb&dl=food-dinner-lunch-70497.jpg&fm=jpg",
    "https://images.pexels.com/photos/461198/pexels-photo-461198.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
    "https://images.pexels.com/photos/5938/food-salad-healthy-lunch.jpg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
    "https://images.pexels.com/photos/5317/food-salad-restaurant-person.jpg?cs=srgb&dl=beverages-brunch-cocktail-5317.jpg&fm=jpg",
    "https://images.pexels.com/photos/5317/food-salad-restaurant-person.jpg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"    

]
random_el = lambda l: l[randint(0,len(l)-1)]

#Change schema for location to GeoPointField
for i in range(0,100):
    lat = round(uniform(20.551303,20.742335),6)
    lon = round(uniform(-103.461074,-103.221499),6)
    restaurant = Restaurant(
        name=str(hash(chr(i))),
        location=[lon,lat],
        city='GDL',
        img_url=random_el(urls)
    ).save()
#restaurant.save()
result = Restaurant.objects(location__geo_within_sphere=[[-103.391922, 20.673566], 3/6371.0])

for r in result:
    print(r['location'])