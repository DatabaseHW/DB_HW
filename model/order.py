from enum import unique
from tokenize import Floatnumber
from unicodedata import category
import bcrypt
from sklearn.utils import check_matplotlib_support
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from configuration import user_database, Login_manager, website
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

from model.shop import Shop
from model.user import User
from model.product import Product

bcrypt = Bcrypt(website)

class Order(user_database.Model, UserMixin):
    __tablename__ = 'orders'
    oid = user_database.Column(user_database.String(256), primary_key = True)
    uid = user_database.Column(user_database.String(256), ForeignKey("users.id"))
    sid = user_database.Column(user_database.String(256), ForeignKey("shops.sid"))
    status = user_database.Column(user_database.String(256))
    start = user_database.Column(user_database.String(256))
    end = user_database.Column(user_database.String(256))
    shop_name = user_database.Column(user_database.String(256), ForeignKey("shops.name"))
    price = user_database.Column(user_database.Integer)


    def __init__(self, uid, sid, status, start, shop_name, price, oid = None, end = ""):
        if oid == None:
            self.oid = bcrypt.generate_password_hash(uid + sid + start) # suck
        else:
            self.oid = oid
        self.uid = uid
        self.sid = sid
        self.status = status
        self.start = start
        self.end = end
        self.shop_name = shop_name
        self.price = price
    
    def __repr__(self):
        return f'<Order {self.oid!r}>'
    
    def __str__(self):
        return f'<Order {self.oid!r}>'