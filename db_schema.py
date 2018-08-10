from mongoengine import Document, StringField,\
                        connect, GeoPointField,\
                        DateTimeField, DecimalField,\
                        ObjectIdField, BooleanField, EmbeddedDocumentListField,\
                        EmbeddedDocument,PointField
import datetime
#Uses dotenv to load user variables
import settings

#TIME STUFF
from datetime import datetime, timedelta

def create_expire(days=30):
    return datetime.utcnow() + timedelta(days=days)

from random import randint
urls = [
    "https://images.pexels.com/photos/70497/pexels-photo-70497.jpeg?cs=srgb&dl=food-dinner-lunch-70497.jpg&fm=jpg",
    "https://images.pexels.com/photos/461198/pexels-photo-461198.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
    "https://images.pexels.com/photos/5938/food-salad-healthy-lunch.jpg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
    "https://images.pexels.com/photos/5317/food-salad-restaurant-person.jpg?cs=srgb&dl=beverages-brunch-cocktail-5317.jpg&fm=jpg",
    "https://images.pexels.com/photos/5317/food-salad-restaurant-person.jpg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"    

]
random_img = lambda l: l[randint(0,len(l)-1)]

class User(Document):
    name            = StringField(required=True)
    mail            = StringField(required=True)
    hash_password   = StringField(required=True)
    credit          = DecimalField(default=0.0)
    complete        = BooleanField(default=False)
    current_location= PointField(required=False, default=[-103.392800,20.675045])
    #password = StringField(require=False)

class Restaurant(Document):
    name            = StringField(required=True)
    location        = PointField(required=True)
    city            = StringField(required=True)
    img_url         = StringField(required=False, default=random_img(urls))
    category        = StringField(required=True, default='Restaurante')
    delivery_cost   = StringField(required=True, default='0')
    category_code   = StringField(required=True)

class Order(Document):
    userID          = ObjectIdField(required=True)
    restaurantID    = ObjectIdField(required=True)
    userLocation    = ObjectIdField(required=True)

class Session(Document):
    userID          = StringField(required=True)
    created_at      = DateTimeField(default=datetime.utcnow)
    expires_at      = DateTimeField(default=create_expire)
    session_hash    = StringField(required=True)

class Location(Document):
    userID          = GeoPointField(required=True)
    uame            = StringField(required=False, default='current')
    description     = StringField(required=False)

class Product(EmbeddedDocument):
    name            = StringField(required=True)
    price           = DecimalField(required=True)
    category        = StringField(required=True) 

class Cart(Document):
    userID          = ObjectIdField(required=True)
    restaurantID    = ObjectIdField(required=True)
    products        = EmbeddedDocumentListField(Product)