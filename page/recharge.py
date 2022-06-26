import base64
from fileinput import filename
from uuid import UUID
from flask import *
from flask_login import *
from numpy import require
from flask_sqlalchemy import *

from configuration import website, user_database
from forms import RechargeForm
from model.shop import Shop
from model.user import User
from model.product import Product

def recharge(Shop_Form, Product_Form, Recharge_Form, searchShops):
    # TODO: edit this file
    delete_user = User.query.filter_by(id = current_user.get_id()).first()
    # print("Recharge_Form.recharge_addvalue", vars(Recharge_Form.recharge_addvalue))
    new_balance = Recharge_Form.recharge_addvalue.data + delete_user.balance
    new_user = User(delete_user.account, delete_user.passwd_hash, delete_user.name, delete_user.phonenumber, delete_user.latitude, delete_user.longitude, new_balance, delete_user.id, passwdHashed = True)

    user_database.session.delete(delete_user)
    user_database.session.add(new_user)

    # add transcation
    # new_transcation = 1
    # user_database.session.add(new_transcation)
    user_database.session.commit()

    # TODO error message: can not be float
    flash("加值成功",category="recharge success")
    return render_template(
                            "nav.html", 
                            user = User.query.filter_by(id=current_user.get_id()).first(), 
                            searchShops = searchShops, 
                            shop_form = Shop_Form,
                            product_form = Product_Form,
                            has_shop=Shop.query.filter_by(uid=current_user.get_id())
                        )
