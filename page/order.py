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

    # print("[27] order_sid.data:", type(Order_Form.order_sid.data))
    # print("[28] calcPrice_total.data:", type(Order_Form.calcPrice_total.data))
    # print("[29] order_submit.data:", type(Order_Form.order_submit.data))
    print("[29] pnum.data:", type(Order_Form.pnum.data))
    print("[29] pnum.data:", Order_Form.pnum.data)

    orderProducts = []
    all_product = Product.query.all()
    productNum = Order_Form.pnum.data
    productNum = productNum.split(' ')
    print("[40] productNum", productNum)
    for x in all_product:
        if(x.sid == order_sid):
            # productNum = request.args.get('productNum' + x.pid) # cannot get number
            # if productNum[0] > 0:
            orderProducts.append(Product(x.sid, x.name, productNum, x.price, x.picture, x.pid))
            productNum.remove(productNum[0])

            # 這邊還沒寫好哦我只是大致寫了一下
            # try:
            #     val = int(productNum)
            # except ValueError:
            #     flash("商品數量非正整數或零",category="order_product_not_pos_int")
            
            
            # if int(Order_Form.calcPrice_total.data) > User.query.filter_by(id = current_user.get_id()).first().balance:
            #     flash("訂購金額 > 餘額",category="order_product_not_enough_money")
            
            # # flash("餐點不存在",category="order_product_no_product")
            
            # if productNum > x.quantity: # productNum is None, so error
            #     flash("商品數量不足",category="order_product_not_enough")

            # return render_template(
            #                         "nav.html", 
            #                         user = User.query.filter_by(id=current_user.get_id()).first(), 
            #                         searchShops = searchShops, 
            #                         shop_form = Shop_Form,
            #                         product_form = Product_Form,
            #                         has_shop=Shop.query.filter_by(uid=current_user.get_id())
            #                     )
        
    # add order
    # (uid, sid, status, start, shop_name, price, oid = None, end = "")
    uid = current_user.get_id()
    start_time = str(date.today()) + ' ' + datetime.now().strftime("%H:%M:%S")
    shopName = Shop.query.filter_by(sid = order_sid).first().name
    total_price = Order_Form.calcPrice_total.data

    # print("[41] start time:", type(start_time), start_time)
    # print("[42] shop_name:", shopName)
    # print("[43] price:", total_price)
    
    # add order
    new_order = Order(uid, order_sid, "Not Finish", start_time, shopName, total_price)
    user_database.session.add(new_order)
    user_database.session.commit()

    # add item
    print("[49] orderProducts:", orderProducts)
    for x in orderProducts:
        new_item = Item(str(new_order.oid), x.pid, x.quantity, x.quantity * x.price)
        new_item = Item(str(new_order.oid), x.pid, 10, x.price) # quantity is none, because product is none
        user_database.session.add(new_item)

        # minus product quantity
        delete_product = Product.query.filter_by(pid = x.pid).first()
        new_product = Product(x.sid, x.name, delete_product.quantity - x.quantity, x.price, x.picture, x.pid)
        # new_product = Product(x.sid, x.name, delete_product.quantity - 1, x.price, x.picture, x.pid) # quantity is none, because product is none 
        user_database.session.delete(delete_product)
        user_database.session.add(new_product)
        user_database.session.commit()

    # add transaction
    sname = Shop.query.filter_by(sid = order_sid).first().name
    uname = User.query.filter_by(id = current_user.get_id()).first().name
    new_transaction1 = Transaction("Payment", start_time, sname, total_price)
    new_transaction2 = Transaction("Receive", start_time, uname, total_price)
    user_database.session.add(new_transaction1)
    user_database.session.add(new_transaction2)
    user_database.session.commit()
    
    flash("訂購成功",category="order_product_success")
    return render_template(
                            "nav.html", 
                            user = User.query.filter_by(id=current_user.get_id()).first(), 
                            searchShops = searchShops, 
                            shop_form = Shop_Form,
                            product_form = Product_Form,
                            has_shop=Shop.query.filter_by(uid=current_user.get_id())
                        )
