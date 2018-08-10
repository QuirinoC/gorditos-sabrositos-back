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

images = ['https://imageshack.com/a/img923/6923/WJbQa0.jpg',
          'https://imageshack.com/a/img924/1564/iIK9Pq.jpg']

promo    = ['']
free     = ['']
mexican  = ['http://imagizer.imageshack.us/a/img924/3096/V6MCXX.jpg',
            'http://imagizer.imageshack.us/a/img922/2568/DfLAIt.jpg',
            'http://imagizer.imageshack.us/a/img922/5255/ZXnsDl.jpg',

        ]
hamburger= ['http://imagizer.imageshack.us/a/img923/3998/oLquvv.jpg',
            'http://imagizer.imageshack.us/a/img921/9595/KEHyf8.jpg',
            'http://imagizer.imageshack.us/a/img924/6021/ygTpJx.jpg']
hotdog   = ['https://www.vvsupremo.com/wp-content/uploads/2016/02/900X570_Mexican-Style-Hot-Dogs.jpg']
pizza    = ['http://imagizer.imageshack.us/a/img922/1473/sDaXuf.jpg',
            'http://imagizer.imageshack.us/a/img921/4346/yXrcmp.jpg',
            'http://imagizer.imageshack.us/a/img923/6822/0eW0lz.jpg']
chinese  = ['http://imagizer.imageshack.us/a/img921/8430/7l2FMu.jpg']
japanese = ['http://imagizer.imageshack.us/a/img924/1951/H6d6PQ.jpg',
            'https://imageshack.com/a/img922/7246/fhsbyH.jpg']
coffee    = ['http://imagizer.imageshack.us/a/img923/1115/v1UACi.jpg',
            'http://imagizer.imageshack.us/a/img921/5471/bmeRFO.jpg']
desserts = ['http://imagizer.imageshack.us/a/img924/8159/Al2xbc.jpg',
            'http://imagizer.imageshack.us/a/img921/6772/cjHh7F.jpg',
            'http://imagizer.imageshack.us/a/img921/5149/hzo8e3.jpg',
            'http://imagizer.imageshack.us/a/img923/1479/TT2l76.jpg',
            'http://imagizer.imageshack.us/a/img923/8657/EDPJ3O.jpg',
            'http://imagizer.imageshack.us/a/img924/421/YUqluN.jpg',
            'http://imagizer.imageshack.us/a/img923/12/Y0j1Lw.jpg',
            'http://imagizer.imageshack.us/a/img922/7710/PZaD10.jpg',
            'http://imagizer.imageshack.us/a/img922/7710/PZaD10.jpg',
            'http://imagizer.imageshack.us/a/img924/1564/iIK9Pq.jpg']
seafood  = ["http://imagizer.imageshack.us/a/img924/5560/mr8X1i.jpg",
            "http://imagizer.imageshack.us/a/img922/7802/mPQZnh.jpg"]

categories = \
[
 #('Promociones', promo,'promo'),
 #('Envio Gratis', free,'free'),
 ('Mexicana', mexican,'mexican'),
 ('Hamburguesas', hamburger,'hamburger'),
 ('Hot Dogs', hotdog,'hotdog'),
 ('Pizza', pizza,'pizza'),
 ('Comida China', chinese,'chinese'),
 ('Japonesa y Sushi', japanese,'japanese'),
 ('Café', coffee,'coffee'),
 ('Postres', desserts,'desserts'),
 ('Mariscos', seafood,'seafood')]

delivery_costs = ['0','25','30','40']

random_el = lambda l: l[randint(0,len(l)-1)]




#Change schema for location to GeoPointField
for i in range(0,200):
    lat = round(uniform(20.551303,20.742335),6)
    lon = round(uniform(-103.461074,-103.221499),6)
    index = randint(0, len(categories)-1)
    restaurant = Restaurant(
        name         =str(hash(chr(i))),
        location     =[lon,lat],
        city         ='GDL',
        img_url      =random_el(categories[index][1]),
        category     =categories[index][0],
        delivery_cost=random_el(delivery_costs),
        category_code=categories[index][2]
    ).save()
#restaurant.save()
#result = Restaurant.objects(location__geo_within_sphere=[[-103.391922, 20.673566], 3/6371.0])

#for r in result:
#    print(r['location'])