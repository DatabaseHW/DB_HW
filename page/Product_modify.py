import base64
from fileinput import filename
from uuid import UUID
from flask import *
from flask_login import *
from numpy import require
from flask_sqlalchemy import *

from configuration import website, user_database
from forms import LoginForm, ShopForm, ProductForm
from model.shop import Shop
from model.user import User
from model.product import Product

def product_modify(Modify_Form, searchShops, shop_product, Shop_Form, Product_Form, searchMyOrder0, searchMyOrder1, searchMyOrder2, searchMyOrder3, searchShopOrder0, searchShopOrder1, searchShopOrder2, searchShopOrder3, searchTransactionRecord0, searchTransactionRecord1, searchTransactionRecord2, searchTransactionRecord3, Location_Form, Recharge_Form):
    delete_product = Product.query.filter_by(pid = Modify_Form.modify_pid.data).first()
    new_product = Product(delete_product.sid, delete_product.name, Modify_Form.quantity_modify.data, Modify_Form.price_modify.data, delete_product.picture, Modify_Form.modify_pid.data)

    user_database.session.delete(delete_product)
    user_database.session.add(new_product)
    user_database.session.commit()

    shop_product = []
    if Shop.query.filter_by(uid = current_user.get_id()).first() != None:
        user_sid = Shop.query.filter_by(uid = current_user.get_id()).first().sid
        shop_product = Product.query.all()
        i = 0
        while i < len(shop_product):
            if(shop_product[i].sid != user_sid):
                shop_product.remove(shop_product[i])
                continue
            i += 1
        for i in range(len(shop_product)):
            shop_product[i].ID = i + 1
        
    print("shop_product:")
    for i in range(len(shop_product)):
        print("shop_product:", shop_product[i])

    flash("修改成功",category="product modify success")
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
