from mongoengine import Document, StringField,
                        connect, GeoPointField,
                        DateTimeField, DecimalField,
                        ObjectIdField
import datetime
#Uses dotenv to load user variables
import settings

#TIME STUFF
from datetime import datetime, timedelta

def create_expire(days=30):
    return datetime.utcnow() + timedelta(days=days)

class User(Document):
    name = StringField(required=True)
    mail = StringField(required=True)
    hash_password = StringField(required=True)
    credit = DecimalField(default=0.0)

class Restaurant(Document):
    name     = StringField(required=True)
    location = StringField(required=True)
    city     = StringField(required=True)

class Order(Document):
    userID   = Object

class Session(Document):
    userID     = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    expires_at = DateTimeField(default=create_expire)

