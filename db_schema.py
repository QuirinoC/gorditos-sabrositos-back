from mongoengine import Document, StringField, connect, GeoPointField
#Uses dotenv to load user variables
import settings

class User(Document):
    name = StringField(required=True)
    mail = StringField(required=True)
    hash_password = StringField(required=True)
    location = GeoPointField(required=False)

class Restaurant(Document):
    name     = StringField(required=True)
    location = StringField(required=True)
    city     = StringField(required=True)



class Order(Document):
    pass

class Session(Document):
    pass