from enum import unique
from tokenize import Floatnumber
from unicodedata import category
import bcrypt
from sklearn.utils import check_matplotlib_support
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from configuration import user_database, Login_manager, website
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

from model.user import User

bcrypt = Bcrypt(website)

class Shop(user_database.Model, UserMixin):
    __tablename__ = 'shops'
    uid = user_database.Column(user_database.String(256), ForeignKey("users.id"))
    sid = user_database.Column(user_database.String(256), primary_key = True)
    name = user_database.Column(user_database.String(64), unique = True)
    latitude = user_database.Column(user_database.Float)
    longitude = user_database.Column(user_database.Float)
    categorys = user_database.Column(user_database.String(64))

    def __init__(self, uid, name, latitude = None, longitude = None, categorys = None, sid = None):
        self.uid = uid
        if(sid == None):
            self.sid = bcrypt.generate_password_hash(name)
        else:
            self.sid = sid
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.categorys = categorys
    
    # @Login_manager.user_loader
    # def load_shop(user_id):
    #     return User.query.get(user_id)

    def __repr__(self):
        return f'<Shop {self.name!r}>'
    
    def __str__(self):
        return f'<Shop {self.name!r} SID {self.sid!r}>'

    def get_id(self):
        return self.sid