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
            orderProducts.append(Product(x.sid, x.name, productNum, x.price, x.picture, x.pid))

    # (uid, sid, status, start, shop_name, price, oid = None, end = "")
    # start time
    start = "1"
    # how to get shop name by sid?
    shopName = Shop.query.filter_by(sid = order_sid).first().name
    # price = request.args.get('calcPrice_total')
    price = Order_Form.calcPrice_total.data
    print("[37] shop_name:", shopName)
    print("[38] price:", price)
    new_order = Order(current_user.get_id(), order_sid, "Not Finish", start, shopName, price)
    print("order:", new_order)

    # add transcation

    user_database.session.add(new_order)
    user_database.session.commit()
    # flash("加值成功",category="order price calculate success")
    return render_template(
                            "nav.html", 
                            user = User.query.filter_by(id=current_user.get_id()).first(), 
                            searchShops = searchShops, 
                            shop_form = Shop_Form,
                            product_form = Product_Form,
                            has_shop=Shop.query.filter_by(uid=current_user.get_id())
                        )
