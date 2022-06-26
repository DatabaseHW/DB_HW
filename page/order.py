import base64
from fileinput import filename
from uuid import UUID
from flask import *
from flask_login import *
from numpy import require
from flask_sqlalchemy import *

from configuration import website, user_database
from forms import OrderForm
from model.shop import Shop
from model.user import User
from model.product import Product
from model.order import Order
from model.item import Item
from model.transaction import Transaction

from datetime import datetime, date


def order(Shop_Form, Product_Form, Order_Form, searchShops):
    # TODO: edit this file
    print("hahah order.py")
    order_sid = Order_Form.order_sid.data

    print("order_sid:", order_sid) # always = None

    orderProducts = []
    all_product = Product.query.all()
    for x in all_product:
        if(x.sid == order_sid):
            productNum = request.args.get('productNum' + x.pid) # cannot get number
            print("[28] index:", 'productNum' + x.pid)
            print("[29] productNum:", productNum)
            print("[35] x.quantity:", x.quantity)
            
            # TODO error detection 
            # if productNum > x.quantity: # productNum is None, so error
            #     flash("商店名稱不可重複",category="name_repeated")
            #     return render_template(
            #                             "nav.html", 
            #                             user = User.query.filter_by(id=current_user.get_id()).first(), 
            #                             searchShops = searchShops, 
            #                             shop_form = Shop_Form,
            #                             product_form = Product_Form,
            #                             has_shop=Shop.query.filter_by(uid=current_user.get_id())
            #                         )
            
            orderProducts.append(Product(x.sid, x.name, productNum, x.price, x.picture, x.pid))

    # (uid, sid, status, start, shop_name, price, oid = None, end = "")
    uid = current_user.get_id()
    start_time = str(date.today()) + ' ' + datetime.now().strftime("%H:%M:%S")
    shopName = Shop.query.filter_by(sid = order_sid).first().name
    total_price = Order_Form.calcPrice_total.data

    # print("[41] start time:", type(start_time), start_time)
    # print("[42] shop_name:", shopName)
    # print("[43] price:", total_price)
    
    new_order = Order(uid, order_sid, "Not Finish", start_time, shopName, total_price)
    user_database.session.add(new_order)
    user_database.session.commit()

    # create item(oid, pid, quantity, price, iid = None)
    print("[49] orderProducts:", orderProducts)
    for x in orderProducts:
        # new_item = Item(new_order.oid, x.pid, x.quantity, x.quantity * x.price)
        # print(type(new_order.oid), type(x.pid))
        new_item = Item(str(new_order.oid), x.pid, 10, x.price) # quantity is none, because product is none
        user_database.session.add(new_item)

        delete_product = Product.query.filter_by(pid = x.pid).first()
        # new_product = Product(x.sid, x.name, delete_product.quantity - x.quantity, x.price, x.picture, x.pid)
        new_product = Product(x.sid, x.name, delete_product.quantity - 1, x.price, x.picture, x.pid) # quantity is none, because product is none 
        user_database.session.delete(delete_product)
        user_database.session.add(new_product)
        
        user_database.session.commit()


    # edit product quantity

    # add transaction
    # (self, action, trans_time, trader_id, change, tid = None)
    
    # new_transaction1 = Transaction("Payment", start_time, order_sid, total_price)
    # new_transaction2 = Transaction("Receive", start_time, uid, total_price)
    # user_database.session.add(new_transaction1)
    # user_database.session.add(new_transaction2)
    
    # user_database.session.commit()
    return render_template(
                            "nav.html", 
                            user = User.query.filter_by(id=current_user.get_id()).first(), 
                            searchShops = searchShops, 
                            shop_form = Shop_Form,
                            product_form = Product_Form,
                            has_shop=Shop.query.filter_by(uid=current_user.get_id())
                        )
