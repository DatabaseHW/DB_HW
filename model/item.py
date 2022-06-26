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
from model.order import Order

from datetime import datetime, date

bcrypt = Bcrypt(website)

class Item(user_database.Model, UserMixin):
    __tablename__ = 'items'
    iid = user_database.Column(user_database.String(256), primary_key = True)
    oid = user_database.Column(user_database.String(256), ForeignKey("orders.oid"))
    pid = user_database.Column(user_database.String(256), ForeignKey("products.pid"))
    quantity = user_database.Column(user_database.Integer)
    price = user_database.Column(user_database.Integer)

    def __init__(self, oid, pid, quantity, price, iid = None):
        if(iid == None):
            self.iid = bcrypt.generate_password_hash(oid + pid)
        else:
            self.iid = iid
        self.oid = oid
        self.pid = pid
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f'<Item {self.name!r}>'
    
    def __str__(self):
        return f'<Item {self.name!r} IID {self.iid!r}>'

    def get_id(self):
        return self.iid