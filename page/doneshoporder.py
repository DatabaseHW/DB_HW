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

def doneshoporder(Shop_Form, Product_Form, DoneShopOrder_Form, searchShops):
    # TODO: edit this file

    # add transcation
    order_id = DoneShopOrder_Form.searchShopOrder_oid.data
    print("[23] oid:", order_id)
    uid = current_user.get_id()
    order_sid = Order.query.filter_by(oid = order_id).first().sid
    sname = Shop.query.filter_by(sid = order_sid).first().name
    uname = User.query.filter_by(id = current_user.get_id()).first().name
    total_price = Order.query.filter_by(oid = order_id).first().price
    end_time = str(date.today()) + ' ' + datetime.now().strftime("%H:%M:%S")

    print("sname:", sname)
    print("uname:", uname)
    print("total_price:", total_price)

    # add transaction
    new_transaction1 = Transaction("Payment", end_time, sname, str(total_price))
    new_transaction2 = Transaction("Receive", end_time, uname, str(total_price))
    user_database.session.add(new_transaction1)
    user_database.session.add(new_transaction2)
    user_database.session.commit()

    # change order status
    delete_order = Order.query.filter_by(oid = order_id).first()
    new_order = Order(uid, order_sid, "Finished", delete_order.start, delete_order.shop_name, total_price, delete_order.oid, end_time)
    user_database.session.delete(delete_order)
    user_database.session.add(new_order)
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
