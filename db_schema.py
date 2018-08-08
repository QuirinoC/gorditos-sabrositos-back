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

class User(Document):
    name            = StringField(required=True)
    mail            = StringField(required=True)
    hash_password   = StringField(required=True)
    credit          = DecimalField(default=0.0)
    complete        = BooleanField(default=False)
    currentLocation = PointField(required=False)
    #password = StringField(require=False)

class Restaurant(Document):
    name            = StringField(required=True)
    location        = PointField(required=True)
    city            = StringField(required=True)

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