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
from model.order import Order
from model.item import Item
from model.transaction import Transaction

from datetime import datetime, date

def cancelshoporder(Shop_Form, Product_Form, CancelShopOrder_Form, searchShops):
    # TODO: edit this file

    # add transcation
    order_id = CancelShopOrder_Form.searchShopOrder_oid.data
    print("[23] oid:", order_id)
    uid = current_user.get_id()
    order_sid = Order.query.filter_by(oid = order_id).first().sid
    total_price = Order.query.filter_by(oid = order_id).first().price
    end_time = str(date.today()) + ' ' + datetime.now().strftime("%H:%M:%S")

    print("total_price:", total_price)

    # modify order status, end_time
    delete_order = Order.query.filter_by(oid = order_id).first()
    new_order = Order(uid, order_sid, "Cancelled", delete_order.start, delete_order.shop_name, total_price, delete_order.oid, end_time)
    print("[35] delete_order:", delete_order)
    print("[36] new_order:", new_order)
    user_database.session.delete(delete_order)
    user_database.session.add(new_order)
    user_database.session.commit()

    # add product quantity
    all_product = Product.query.all()
    all_item = Item.query.all()
    for x in all_product:
        for y in all_item:
            if x.pid == y.pid:
                delete_product = Product.query.filter_by(pid = x.pid).first()
                new_product = Product(x.sid, x.name, x.quantity + y.quantity, x.price, x.picture, x.pid)
                user_database.session.delete(delete_product)
                user_database.session.add(new_product)
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
