from enum import unique
from tokenize import Floatnumber
import bcrypt
from sklearn.utils import check_matplotlib_support
from sqlalchemy import Column, Integer, Numeric, String
from configuration import user_database, Login_manager
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from configuration import website

bcrypt = Bcrypt(website)

class User(user_database.Model, UserMixin):
    __tablename__ = 'users'
    id = user_database.Column(user_database.String(256), primary_key = True)
    account = user_database.Column(user_database.String(64), unique = True)
    passwd_hash = user_database.Column(user_database.String(256))
    name = user_database.Column(user_database.String(64))
    phonenumber = user_database.Column(user_database.String(10), unique = True)
    latitude = user_database.Column(user_database.Float)
    longitude = user_database.Column(user_database.Float)

    def __init__(self, account, passwd, name, phone = None, latitude = None, longitude = None):
        self.id = bcrypt.generate_password_hash(account)
        self.name = name
        self.account = account
        self.passwd_hash = bcrypt.generate_password_hash(passwd)
        self.phonenumber = phone
        self.latitude = latitude
        self.longitude = longitude

    def check_password(self,passwd):
        return bcrypt.check_password_hash(self.passwd_hash,passwd)
    
    @Login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    def __repr__(self):
        return f'<User {self.name!r}>'
    
    def __str__(self):
        return f'<User {self.name!r} ID {self.id!r}>'