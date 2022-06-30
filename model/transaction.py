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
from datetime import datetime, date

bcrypt = Bcrypt(website)

class Transaction(user_database.Model, UserMixin):
    __tablename__ = 'transactions'
    # rid 
    tid = user_database.Column(user_database.String(256), primary_key = True)
    uid = user_database.Column(user_database.String(256), ForeignKey("users.id"))
    action = user_database.Column(user_database.String(256))
    trans_time = user_database.Column(user_database.String(256))
    trader = user_database.Column(user_database.String(256))
    change = user_database.Column(user_database.Integer)
    tmp_id = user_database.Column(user_database.String(256))

    def __init__(self, uid, action, trans_time, trader, change, tid = None, tmp_id = None): # TODO
        if(tid == None):
            self.tid = bcrypt.generate_password_hash(uid + action + trans_time + trader + str(change))
        else:
            self.tid = tid
        self.uid = uid
        self.action = action
        self.trans_time = trans_time
        self.trader_id = trader
        self.change = change
        if(tmp_id == None):
            self.tmp_id = bcrypt.generate_password_hash(uid + action + trans_time + trader + str(change) + str(date.today()) + ' ' + datetime.now().strftime("%H:%M:%S"))
        else:
            self.tmp_id = tmp_id

    def __repr__(self):
        return f'<Transaction {self.tid!r}>'
    
    def __str__(self):
        return f'<Transaction {self.tid!r} TID {self.tid!r}>'

    def get_id(self):
        return self.tid