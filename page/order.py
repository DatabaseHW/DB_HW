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

def searchmyorder():
    searchMyOrder0 = Order.query.all()
    searchMyOrder1 = Order.query.all()
    searchMyOrder2 = Order.query.all()
    searchMyOrder3 = Order.query.all()
    
    for _ in range(len(searchMyOrder0)):
        x = searchMyOrder0[_]
        order = Order(x.uid, x.sid, x.status, x.start, x.shop_name, x.price, x.oid, x.end, "1")
        searchMyOrder0[_] = order
        searchMyOrder0[_].ID = _ + 1
    for _ in range(len(searchMyOrder1)):
        x = searchMyOrder1[_]
        order = Order(x.uid, x.sid, x.status, x.start, x.shop_name, x.price, x.oid, x.end, "2")
        searchMyOrder1[_] = order
        searchMyOrder1[_].ID = _ + 1
    for _ in range(len(searchMyOrder2)):
        x = searchMyOrder2[_]
        order = Order(x.uid, x.sid, x.status, x.start, x.shop_name, x.price, x.oid, x.end, "3")
        searchMyOrder2[_] = order
        searchMyOrder2[_].ID = _ + 1
    for _ in range(len(searchMyOrder3)):
        x = searchMyOrder3[_]
        order = Order(x.uid, x.sid, x.status, x.start, x.shop_name, x.price, x.oid, x.end, "4")
        searchMyOrder3[_] = order
        searchMyOrder3[_].ID = _ + 1
    
    all_items = Item.query.all()
    for i in range(len(searchMyOrder0)):
        searchMyOrder0[i].products = []
        searchMyOrder1[i].products = []
        searchMyOrder2[i].products = []
        searchMyOrder3[i].products = []
        for y in all_items:
            if searchMyOrder0[i].oid == y.oid:
                prod = Product.query.filter_by(pid=y.pid).first()
                new_product0 = Product(prod.sid, prod.name, y.quantity, prod.price, prod.picture, prod.pid, "1")
                new_product1 = Product(prod.sid, prod.name, y.quantity, prod.price, prod.picture, prod.pid, "2")
                new_product2 = Product(prod.sid, prod.name, y.quantity, prod.price, prod.picture, prod.pid, "3")
                new_product3 = Product(prod.sid, prod.name, y.quantity, prod.price, prod.picture, prod.pid, "4")
                searchMyOrder0[i].products.append(new_product0)
                searchMyOrder1[i].products.append(new_product1)
                searchMyOrder2[i].products.append(new_product2)
                searchMyOrder3[i].products.append(new_product3)
                # print("[148] searchMyOrder0[i].products", searchMyOrder0[i].products)

    i = 0
    while(i < len(searchMyOrder0)):
        if((searchMyOrder0[i].uid != current_user.get_id())):
            searchMyOrder0.remove(searchMyOrder0[i])
            continue
        i += 1
    i = 0
    while(i < len(searchMyOrder1)):
        if((searchMyOrder1[i].uid != current_user.get_id())):
            searchMyOrder1.remove(searchMyOrder1[i])
            continue
        i += 1
    i = 0
    while(i < len(searchMyOrder2)):
        if((searchMyOrder2[i].uid != current_user.get_id())):
            searchMyOrder2.remove(searchMyOrder2[i])
            continue
        i += 1
    i = 0
    while(i < len(searchMyOrder3)):
        if((searchMyOrder3[i].uid != current_user.get_id())):
            searchMyOrder3.remove(searchMyOrder3[i])
            continue
        i += 1
        
    # if status == 1: # Not Finish
    i = 0
    while(i < len(searchMyOrder1)):
        if((searchMyOrder1[i].status != "Not Finish")):
            searchMyOrder1.remove(searchMyOrder1[i])
            continue
        i += 1
    # elif status == 2: # Finished
    i = 0
    while(i < len(searchMyOrder2)):
        if((searchMyOrder2[i].status != "Finished")):
            searchMyOrder2.remove(searchMyOrder2[i])
            continue
        i += 1
    # elif status == 3: # Cancelled
    i = 0
    while(i < len(searchMyOrder3)):
        if((searchMyOrder3[i].status != "Cancelled")):
            searchMyOrder3.remove(searchMyOrder3[i])
            continue
        i += 1

    for _ in range(len(searchMyOrder0)):
        searchMyOrder0[_].ID = _ + 1
    for _ in range(len(searchMyOrder1)):
        searchMyOrder1[_].ID = _ + 1
    for _ in range(len(searchMyOrder2)):
        searchMyOrder2[_].ID = _ + 1
    for _ in range(len(searchMyOrder3)):
        searchMyOrder3[_].ID = _ + 1

    # print("searchMyOrder:")
    # for _ in range(len(searchMyOrder0)):
    #     print("[194]", searchMyOrder0[_].ID)
    # print("-------------------")
    # for _ in range(len(searchMyOrder1)):
    #     print("[195]", searchMyOrder1[_].ID)
    # print("-------------------")
    # for _ in range(len(searchMyOrder2)):
    #     print("[196]", searchMyOrder2[_].ID)
    # print("-------------------")
    # for _ in range(len(searchMyOrder3)):
    #     print("[197]", searchMyOrder3[_].ID)

    return searchMyOrder0, searchMyOrder1, searchMyOrder2, searchMyOrder3

def searchshoporder():
    searchShopOrder = Order.query.all()
    if Shop.query.filter_by(uid = current_user.get_id()).first() == None:
        return [], [], [], []

    sid = Shop.query.filter_by(uid = current_user.get_id()).first().sid
    
    i = 0
    while(i < len(searchShopOrder)):
        if((searchShopOrder[i].sid != sid)):
            searchShopOrder.remove(searchShopOrder[i])
            continue
        i += 1
    
    searchShopOrder0 = []
    searchShopOrder1 = []
    searchShopOrder2 = []
    searchShopOrder3 = []
    for x in searchShopOrder:
        searchShopOrder0.append(x)
        searchShopOrder1.append(x)
        searchShopOrder2.append(x)
        searchShopOrder3.append(x)
        
    # print("[147] num of searcMyOrder:", len(searchShopOrder))
    # print("[148] status:", type(status), status)

    for _ in range(len(searchShopOrder0)):
        x = searchShopOrder0[_]
        order = Order(x.uid, x.sid, x.status, x.start, x.shop_name, x.price, x.oid, x.end, "1") # need change "1"
        searchShopOrder0[_] = order
        searchShopOrder0[_].ID = _ + 1
    for _ in range(len(searchShopOrder1)):
        x = searchShopOrder1[_]
        order = Order(x.uid, x.sid, x.status, x.start, x.shop_name, x.price, x.oid, x.end, "2")
        searchShopOrder1[_] = order
        searchShopOrder1[_].ID = _ + 1
    for _ in range(len(searchShopOrder2)):
        x = searchShopOrder2[_]
        order = Order(x.uid, x.sid, x.status, x.start, x.shop_name, x.price, x.oid, x.end, "3")
        searchShopOrder2[_] = order
        searchShopOrder2[_].ID = _ + 1
    for _ in range(len(searchShopOrder3)):
        x = searchShopOrder3[_]
        order = Order(x.uid, x.sid, x.status, x.start, x.shop_name, x.price, x.oid, x.end, "4")
        searchShopOrder3[_] = order
        searchShopOrder3[_].ID = _ + 1
    
    all_items = Item.query.all()
    for i in range(len(searchShopOrder0)):
        searchShopOrder0[i].products = []
        searchShopOrder1[i].products = []
        searchShopOrder2[i].products = []
        searchShopOrder3[i].products = []
        for y in all_items:
            if searchShopOrder0[i].oid == y.oid:
                prod = Product.query.filter_by(pid=y.pid).first()
                new_product = Product(prod.sid, prod.name, y.quantity, prod.price, prod.picture, prod.pid)
                searchShopOrder0[i].products.append(new_product)
                searchShopOrder1[i].products.append(new_product)
                searchShopOrder2[i].products.append(new_product)
                searchShopOrder3[i].products.append(new_product)
                # print("[135] searchShopOrder[", i, "].products:", searchShopOrder[i].products)

    # if status == 1: # Not Finish
    i = 0
    while(i < len(searchShopOrder1)):
        if((searchShopOrder1[i].status != "Not Finish")):
            searchShopOrder1.remove(searchShopOrder1[i])
            continue
        i += 1
    # elif status == 2: # Finished
    i = 0
    while(i < len(searchShopOrder2)):
        if((searchShopOrder2[i].status != "Finished")):
            searchShopOrder2.remove(searchShopOrder2[i])
            continue
        i += 1
    # elif status == 3: # Cancelled
    i = 0
    while(i < len(searchShopOrder3)):
        if((searchShopOrder3[i].status != "Cancelled")):
            searchShopOrder3.remove(searchShopOrder3[i])
            continue
        i += 1
    
    for _ in range(len(searchShopOrder0)):
        searchShopOrder0[_].ID = _ + 1
    for _ in range(len(searchShopOrder1)):
        searchShopOrder1[_].ID = _ + 1
    for _ in range(len(searchShopOrder2)):
        searchShopOrder2[_].ID = _ + 1
    for _ in range(len(searchShopOrder3)):
        searchShopOrder3[_].ID = _ + 1

    # print("searchShopOrder:")
    # for _ in range(len(searchShopOrder0)):
    #     print(searchShopOrder0[_].ID)
    # print("-------------------")
    # for _ in range(len(searchShopOrder1)):
    #     print(searchShopOrder1[_].ID)
    # print("-------------------")
    # for _ in range(len(searchShopOrder2)):
    #     print(searchShopOrder2[_].ID)
    # print("-------------------")
    # for _ in range(len(searchShopOrder3)):
    #     print(searchShopOrder3[_].ID)

    # print("[168]", len(searchShopOrder0), len(searchShopOrder1), len(searchShopOrder2), len(searchShopOrder3))

    # for _ in range(len(searchShopOrder0)):
    #     print(searchShopOrder0[_].ID)

    return searchShopOrder0, searchShopOrder1, searchShopOrder2, searchShopOrder3

def searchtransactionrecord():
    searchTransactionRecord = Transaction.query.all()
    uid = current_user.get_id()
    
    i = 0
    while(i < len(searchTransactionRecord)):
        if((searchTransactionRecord[i].uid != uid)):
            searchTransactionRecord.remove(searchTransactionRecord[i])
            continue
        i += 1

    searchTransactionRecord0 = []
    searchTransactionRecord1 = []
    searchTransactionRecord2 = []
    searchTransactionRecord3 = []
    for x in searchTransactionRecord:
        searchTransactionRecord0.append(x)
        searchTransactionRecord1.append(x)
        searchTransactionRecord2.append(x)
        searchTransactionRecord3.append(x)
        
    i = 0
    while(i < len(searchTransactionRecord1)):
        if((searchTransactionRecord1[i].action != "Payment")):
            searchTransactionRecord1.remove(searchTransactionRecord1[i])
            continue
        i += 1
    i = 0
    while(i < len(searchTransactionRecord2)):
        if((searchTransactionRecord2[i].action != "Receive")):
            searchTransactionRecord2.remove(searchTransactionRecord2[i])
            continue
        i += 1
    i = 0
    while(i < len(searchTransactionRecord3)):
        if((searchTransactionRecord3[i].action != "Recharge")):
            searchTransactionRecord3.remove(searchTransactionRecord3[i])
            continue
        i += 1

    for _ in range(len(searchTransactionRecord0)):
        x = searchTransactionRecord0[_]
        transaction = Transaction(x.uid, x.action, x.trans_time, x.trader, x.change, x.tid, "1")
        searchTransactionRecord0[_] = transaction
        searchTransactionRecord0[_].ID = _ + 1
    for _ in range(len(searchTransactionRecord1)):
        x = searchTransactionRecord1[_]
        transaction = Transaction(x.uid, x.action, x.trans_time, x.trader, x.change, x.tid, "2")
        searchTransactionRecord1[_] = transaction
        searchTransactionRecord1[_].ID = _ + 1
    for _ in range(len(searchTransactionRecord2)):
        x = searchTransactionRecord2[_]
        transaction = Transaction(x.uid, x.action, x.trans_time, x.trader, x.change, x.tid, "3")
        searchTransactionRecord2[_] = transaction
        searchTransactionRecord2[_].ID = _ + 1
    for _ in range(len(searchTransactionRecord3)):
        x = searchTransactionRecord3[_]
        transaction = Transaction(x.uid, x.action, x.trans_time, x.trader, x.change, x.tid, "4")
        searchTransactionRecord3[_] = transaction
        searchTransactionRecord3[_].ID = _ + 1

    return searchTransactionRecord0, searchTransactionRecord1, searchTransactionRecord2, searchTransactionRecord3

def order(Order_Form, searchShops, shop_product, Shop_Form, Product_Form, searchMyOrder0, searchMyOrder1, searchMyOrder2, searchMyOrder3, searchShopOrder0, searchShopOrder1, searchShopOrder2, searchShopOrder3, searchTransactionRecord0, searchTransactionRecord1, searchTransactionRecord2, searchTransactionRecord3, Location_Form, Recharge_Form):
    # TODO: edit this file
    order_sid = Order_Form.order_sid.data

    orderProducts = []
    all_product = Product.query.all()
    all_pnum = []
    all_pnum.append(Order_Form.pnum1.data)
    all_pnum.append(Order_Form.pnum2.data)
    all_pnum.append(Order_Form.pnum3.data)
    all_pnum.append(Order_Form.pnum4.data)
    all_pnum.append(Order_Form.pnum5.data)
    all_pnum.append(Order_Form.pnum6.data)
    all_pnum.append(Order_Form.pnum7.data)
    all_pnum.append(Order_Form.pnum8.data)
    all_pnum.append(Order_Form.pnum9.data)
    all_pnum.append(Order_Form.pnum10.data)
    print("all_pnum:", all_pnum[0], all_pnum[1])
    i = 0
    while i < len(all_pnum):
        if all_pnum[i] == None:
            all_pnum.remove(all_pnum[i])
            continue
        all_pnum[i] = all_pnum[i].split(' ')
        if order_sid == all_pnum[i][0]:
            all_pnum[i].remove(all_pnum[i][0])
            productNum = all_pnum[i]
            break
        i += 1
    
    # productNum = "3 "
    print("[339] productNum:", productNum)
    # productNum = productNum.split(' ')

    cnt = 0
    for x in all_product:
        if(x.sid == order_sid):
            cnt += 1
    productNum = productNum[len(productNum)-cnt-1:len(productNum)-1]
    print("[40] productNum", productNum)

    fg = 0
    for x in productNum:
        if x != '0':
            fg = 1
            break
    if fg == 0:
        flash("商品數量非正整數",category="order_product_not_pos_int")
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


    for x in all_product:
        if(x.sid == order_sid):
            # productNum = request.args.get('productNum' + x.pid) # cannot get number
            print("[342] productNum[0]", productNum[0])
            # 這邊還沒寫好哦我只是大致寫了一下
            
            # try:
            #     val = int(productNum[0])
            # except:
            #     flash("商品數量非正整數",category="order_product_not_pos_int")
            #     return render_template(
            #                             "nav.html", 
            #                             # old version is outerjoin in next line
            #                             shop_product = shop_product,
            #                             user = User.query.filter_by(id=current_user.get_id()).first(), 
            #                             has_shop=Shop.query.filter_by(uid=current_user.get_id()).first(),
            #                             searchShops = searchShops, 
            #                             shop_form = Shop_Form, 
            #                             product_form = Product_Form, 
            #                             searchMyOrders0 = searchMyOrder0, 
            #                             searchMyOrders1 = searchMyOrder1, 
            #                             searchMyOrders2 = searchMyOrder2, 
            #                             searchMyOrders3 = searchMyOrder3, 
            #                             searchShopOrders0 = searchShopOrder0, 
            #                             searchShopOrders1 = searchShopOrder1, 
            #                             searchShopOrders2 = searchShopOrder2, 
            #                             searchShopOrders3 = searchShopOrder3, 
            #                             searchTransactionRecords0 = searchTransactionRecord0, 
            #                             searchTransactionRecords1 = searchTransactionRecord1, 
            #                             searchTransactionRecords2 = searchTransactionRecord2, 
            #                             searchTransactionRecords3 = searchTransactionRecord3, 
            #                             location_form = Location_Form, 
            #                 recharge_form = Recharge_Form 
            #                         )
            
            if int(Order_Form.calcPrice_total.data) > User.query.filter_by(id = current_user.get_id()).first().balance:
                flash("訂購金額 > 餘額",category="order_product_not_enough_money")
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
            
            # flash("餐點不存在",category="order_product_no_product")
            
            if int(productNum[0]) > x.quantity: # productNum is None, so error
                flash("商品數量不足",category="order_product_not_enough")
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

            orderProducts.append(Product(x.sid, x.name, int(productNum[0]), x.price, x.picture, x.pid))
            productNum.remove(productNum[0])
        
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
        # new_item = Item(str(new_order.oid), x.pid, 10, x.price) # quantity is none, because product is none
        user_database.session.add(new_item)
        user_database.session.commit()

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
    obj_uid = Shop.query.filter_by(sid = order_sid).first().uid
    new_transaction1 = Transaction(uid, "Payment", start_time, sname, total_price)
    new_transaction2 = Transaction(obj_uid, "Receive", start_time, uname, total_price)
    user_database.session.add(new_transaction1)
    user_database.session.add(new_transaction2)
    user_database.session.commit()

    searchMyOrder0, searchMyOrder1, searchMyOrder2, searchMyOrder3 = searchmyorder()
    searchShopOrder0, searchShopOrder1, searchShopOrder2, searchShopOrder3 = searchshoporder()
    searchTransactionRecord0, searchTransactionRecord1, searchTransactionRecord2, searchTransactionRecord3 = searchtransactionrecord()
    
    flash("訂購成功",category="order_product_success")
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
