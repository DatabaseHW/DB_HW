from argparse import Action
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

bcrypt = Bcrypt(website)

class Transaction(user_database.Model, UserMixin):
    __tablename__ = 'transactions'
    tid = user_database.Column(user_database.String(256), primary_key = True)
    # rid = 
    action = user_database.Column(user_database.String(256))
    time = user_database.Column(user_database.String(256))
    trader = user_database.Column(user_database.String(256), ForeignKey("orders.name"))
    change = user_database.Column(user_database.Integer)

    def __init__(self, oid, pid, quantity, price, iid = None): # TODO
        if(iid == None):
            self.iid = bcrypt.generate_password_hash(oid + pid)
        else:
            self.iid = iid
        self.oid = oid
        self.pid = pid
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f'<Transaction {self.tid!r}>'
    
    def __str__(self):
        return f'<Transaction {self.tid!r} TID {self.tid!r}>'

    def get_id(self):
        return self.tid