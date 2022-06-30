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
from datetime import datetime, date

bcrypt = Bcrypt(website)

class Product(user_database.Model, UserMixin):
    __tablename__ = 'products'
    sid = user_database.Column(user_database.String(256), ForeignKey("shops.sid"))
    pid = user_database.Column(user_database.String(256), primary_key = True)
    name = user_database.Column(user_database.String(64))
    quantity = user_database.Column(user_database.Integer)
    price = user_database.Column(user_database.Integer)
    picture = user_database.Column(user_database.Text)
    tmp_id = user_database.Column(user_database.String(256))

    def __init__(self, sid, name, quantity, price, picture = None, pid = None, tmp_id = None):
        self.sid = sid
        if(pid == None):
            self.pid = bcrypt.generate_password_hash(name + sid)
        else:
            self.pid = pid
        self.name = name
        self.quantity = quantity
        self.price = price
        self.picture = picture
        if(tmp_id == None):
            self.tmp_id = bcrypt.generate_password_hash(name + sid + str(date.today()) + ' ' + datetime.now().strftime("%H:%M:%S"))
        else:
            self.tmp_id = tmp_id
    
    # @Login_manager.user_loader
    # def load_shop(user_id):
    #     return User.query.get(user_id)

    def __repr__(self):
        return f'<Product {self.name!r}>'
    
    def __str__(self):
        return f'<Product {self.name!r} PID {self.pid!r}>'

    def get_id(self):
        return self.pid