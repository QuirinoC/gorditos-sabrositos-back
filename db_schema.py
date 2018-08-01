from mongoengine import Document, StringField, connect
#Uses dotenv to load user variables
import settings

class User(Document):
    name = StringField(required=True),
    mail = StringField(required=True),
    hash_password = StringField(required=True),

class Restaurant(Document):
    pass

class Order(Document):
    pass

class Session(Document):
    pass