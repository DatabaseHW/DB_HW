import base64
from fileinput import filename
from uuid import UUID
from flask import *
from flask_login import *
from numpy import require
from flask_sqlalchemy import *

from configuration import website, user_database
from forms import LocationForm
from model.shop import Shop
from model.user import User
from model.product import Product

def location_modify(Location_Form, searchShops, shop_product, Shop_Form, Product_Form, searchMyOrder0, searchMyOrder1, searchMyOrder2, searchMyOrder3, searchShopOrder0, searchShopOrder1, searchShopOrder2, searchShopOrder3, searchTransactionRecord0, searchTransactionRecord1, searchTransactionRecord2, searchTransactionRecord3, Recharge_Form):
    # TODO: edit this file
    delete_user = User.query.filter_by(id = current_user.get_id()).first()
    new_user = User(delete_user.account, delete_user.passwd_hash, delete_user.name, delete_user.phonenumber, Location_Form.latitude_modify.data, Location_Form.longitude_modify.data, delete_user.balance, delete_user.id, passwdHashed = True)

    # print("change location success")
    
    user_database.session.delete(delete_user)
    user_database.session.add(new_user)
    user_database.session.commit()
    flash("修改成功",category="location modify success")
    return render_template(
                            "nav.html", 
                            # old version is outerjoin in next line
                            shop_product = shop_product,
                            user = User.query.filter_by(id=current_user.get_id()).first(), 
                            has_shop=Shop.query.filter_by(uid=current_user.get_id()).first(),
                            searchShops = searchShops, 
                            shop_form = Shop_Form, 
                            product_form = Product_Form, 
                            searchMyOrders0 = searchMyOrder0, 
                            searchMyOrders1 = searchMyOrder1, 
                            searchMyOrders2 = searchMyOrder2, 
                            searchMyOrders3 = searchMyOrder3, 
                            searchShopOrders0 = searchShopOrder0, 
                            searchShopOrders1 = searchShopOrder1, 
                            searchShopOrders2 = searchShopOrder2, 
                            searchShopOrders3 = searchShopOrder3, 
                            searchTransactionRecords0 = searchTransactionRecord0, 
                            searchTransactionRecords1 = searchTransactionRecord1, 
                            searchTransactionRecords2 = searchTransactionRecord2, 
                            searchTransactionRecords3 = searchTransactionRecord3, 
                            location_form = Location_Form, 
                            recharge_form = Recharge_Form 
                        )
