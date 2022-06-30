import base64
from fileinput import filename
from uuid import UUID
from flask import *
from flask_login import *
from numpy import require
import pymysql.cursors 
from flask_sqlalchemy import *

from configuration import website, user_database
from forms import LoginForm, ModifyForm, ShopForm, ProductForm, DeleteForm, RechargeForm, LocationForm, OrderForm, CancelMyOrderForm, CancelShopOrderForm, DoneShopOrderForm
from model.order import Order #, OrderCalcPriceForm
from model.shop import Shop
from model.user import User
from model.product import Product
from model.item import Item
from model.transaction import Transaction

import bcrypt
from flask_bcrypt import Bcrypt
# from page.myorder import myorder
# from page.orderCalcPrice import orderCalcPrice
from page.order import order
from page.location_modify import location_modify
from page.recharge import recharge
from page.shop_register import shop_register
from page.Product_add import product_add
from page.Product_delete import product_delete
from page.Product_modify import product_modify
from page.cancelmyorder import cancelmyorder
from page.cancelshoporder import cancelshoporder
from page.doneshoporder import doneshoporder

from inspect import currentframe, getframeinfo

from math import radians, cos, sin, asin, sqrt
# import math

import re

def comp(big, small):
    if(small == "" or str(type(small)) == "<class 'NoneType'>"):
        return True
    big = big.lower()
    small = small.lower()
    if(re.search(small, big, 0) == None):
        return False
    else:
        return True

def shop_comp(shop, searchShops):
    i = 0
    while(i < len(searchShops)):
        if(not comp(searchShops[i].name, shop)):
            searchShops.remove(searchShops[i])
            continue
        i += 1
    return searchShops

def meal_comp(meal, searchShops):
    allow_list = []
    all_product = Product.query.all()
    for x in all_product:
        if(comp(x.name, meal)):
            allow_list.append(x.sid)
    i = 0
    while(i < len(searchShops)):
        if((searchShops[i].sid not in allow_list)):
            searchShops.remove(searchShops[i])
            continue
        i += 1
    return searchShops

def cate_comp(cate, searchShops):
    i = 0
    while(i < len(searchShops)):
        if(not comp(searchShops[i].categorys, cate)):
            searchShops.remove(searchShops[i])
            continue
        i += 1
    return searchShops


def distance_range(distance_value):
    return { 'not concerned' : (0, 40008000), 'near' : (0, 1000), 'medium' : (1000, 10000), 'far' : (10000, 40008000) }.get(distance_value)

def distance_level(distance_value):
    if(distance_value < 1000): return "near"
    if(distance_value < 10000): return "medium"
    return "far"
    
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r * 1000

# bcrypt = Bcrypt(website)

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


def searchshoporder_(status):
    searchShopOrder = Order.query.all()
    # sid = request.args.get('shopid')
    sid = Shop.query.filter_by(uid=current_user.get_id()).first().sid
    print("[158] sid:", sid)
    
    i = 0
    while(i < len(searchShopOrder)):
        if((searchShopOrder[i].sid != sid)):
            searchShopOrder.remove(searchShopOrder[i])
            continue
        i += 1

    if status == 1: # Not Finish
        i = 0
        while(i < len(searchShopOrder)):
            if((searchShopOrder[i].status != "Not Finish")):
                searchShopOrder.remove(searchShopOrder[i])
                continue
            i += 1
    elif status == 2: # Finished
        i = 0
        while(i < len(searchShopOrder)):
            if((searchShopOrder[i].status != "Finished")):
                searchShopOrder.remove(searchShopOrder[i])
                continue
            i += 1
    elif status == 3: # Cancelled
        i = 0
        while(i < len(searchShopOrder)):
            if((searchShopOrder[i].status != "Cancelled")):
                searchShopOrder.remove(searchShopOrder[i])
                continue
            i += 1
    
    all_items = Item.query.all()
    for i in range(len(searchShopOrder)):
        searchShopOrder[i].products = []
        for y in all_items:
            if searchShopOrder[i].oid == y.oid:
                prod = Product.query.filter_by(pid=y.pid).first()
                new_product = Product(prod.sid, prod.name, y.quantity, prod.price, prod.picture, prod.pid)
                searchShopOrder[i].products.append(new_product)
                # print("[135] searchShopOrder[", i, "].products:", searchShopOrder[i].products)

    for _ in range(len(searchShopOrder)):
        searchShopOrder[_].ID = _ + 1

    return searchShopOrder
    

@website.route('/<int:status>', methods = ['GET','POST'])
@login_required
def homee(status=3):
    print("homee called Status: ",type(status),status)
    try:
        status = int(status)
    except:
        status = int(status[1])
    
    #initianl searchShops
    searchShops = Shop.query.all()

    shop = request.args.get('shopname')
    meal = request.args.get('meal')
    category = request.args.get('category')

    searchShops = shop_comp(shop, searchShops)
    searchShops = meal_comp(meal, searchShops)
    searchShops = cate_comp(category, searchShops)

    # print("[120] searchshops:", searchShops)

    # distance
    # print(type(User.query.all()), User.query.all())
    # print(User.query.filter_by(id=current_user.get_id()).first(), User.query.filter_by(id=current_user.get_id()).all(), User.query.filter_by(id=current_user.get_id()))
    # print("[187] type ", type(request.args.get('distance')), request.args.get('distance'))
    if str(type(request.args.get('distance'))) == "<class 'str'>":
        distanceL, distanceU = distance_range(request.args.get('distance'))
        remove_list = []
        # points = [(x.latitude, x.longitude) for x in searchShops] # Shop.query.all() for all shop
        for x in searchShops:
            lat = x.latitude
            lon = x.longitude
            dis = haversine(lat, lon, User.query.filter_by(id=current_user.get_id()).all()[0].latitude, User.query.filter_by(id=current_user.get_id()).all()[0].longitude)
            if(dis < distanceL or dis >= distanceU):
                remove_list.append(x)
        for x in remove_list:
            searchShops.remove(x)

    for x in searchShops:
        lat = x.latitude
        lon = x.longitude
        dis = haversine(lat, lon, User.query.filter_by(id=current_user.get_id()).all()[0].latitude, User.query.filter_by(id=current_user.get_id()).all()[0].longitude)
        x.distance = distance_level(dis)
        x.deliveryFee = max(10, round(dis*0.01))

    # price
    priceL = request.args.get('priceL')
    priceU = request.args.get('priceU')
    if(str(type(request.args.get('priceL'))) == "<class 'str'>" and priceL != ""):
        if(priceL.isnumeric()):
            priceL = int(priceL)
        else:
            priceL = 1e51
    else:
        priceL = 0
    if(str(type(request.args.get('priceU'))) == "<class 'str'>" and priceU != ""):
        if(priceU.isnumeric()):
            priceU = int(priceU)
        else:
            priceU = -1
    else:
        priceU = 1e50

    if((str(type(priceL)) == "<class 'int'>" or str(type(priceL)) == "<class 'float'>") and (str(type(priceU)) == "<class 'int'>" or str(type(priceU)) == "<class 'float'>")):
        allow_list = []
        all_product = Product.query.all()
        # print('[162] allproduct:', all_product)
        for x in all_product:
            if(priceL <= x.price and x.price <= priceU):
                allow_list.append(x.sid)
            
        # print("[167] allow_list:", allow_list)
        # print("[168] searchshops:", searchShops)

        i = 0
        while(i < len(searchShops)):
            if((searchShops[i].sid not in allow_list)):
                searchShops.remove(searchShops[i])
                continue
            i += 1
        
        # print("[177] searchshops:", searchShops)

    all_product = Product.query.all()
    for y in searchShops:
        y.products = []
    
    for x in all_product:
        for y in searchShops:
            if(y.sid == x.sid):
                y.products.append(x)

    # for y in searchShops:
    #     print("[191] itme in searchShops", y)
    
    # print("[186] all:", Shop.query.all())
    # print("[270] searchShops:", searchShops.pro)
    for _ in range(len(searchShops)):
        # print("[191] vars:", vars(searchShops[_]))
        searchShops[_].ID = _ + 1
        # if(searchShops[_].deliveryFee):
            # print("deliveryFee:", searchShops[_].deliveryFee)

    searchMyOrder0, searchMyOrder1, searchMyOrder2, searchMyOrder3 = searchmyorder()
    searchShopOrder0, searchShopOrder1, searchShopOrder2, searchShopOrder3 = searchshoporder()
    searchTransactionRecord0, searchTransactionRecord1, searchTransactionRecord2, searchTransactionRecord3 = searchtransactionrecord()

    # for x in searchMyOrder0:
    #     print(x)
    # print("--------------------------------")
    # for x in searchMyOrder1:
    #     print(x)
    # print("--------------------------------")
    # for x in searchMyOrder2:
    #     print(x)
    # print("--------------------------------")
    # for x in searchMyOrder3:
    #     print(x)
    # print("--------------------------------")

    # for x in searchShopOrder0:
    #     print(x)
    # print("--------------------------------")
    # for x in searchShopOrder1:
    #     print(x)
    # print("--------------------------------")
    # for x in searchShopOrder2:
    #     print(x)
    # print("--------------------------------")
    # for x in searchShopOrder3:
    #     print(x)
    # print("--------------------------------")

    # my order list
    CancelMyOrder_Form = CancelMyOrderForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    CancelShopOrder_Form = CancelShopOrderForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    DoneShopOrder_Form = DoneShopOrderForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    Order_Form = OrderForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    Location_Form = LocationForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    Recharge_Form = RechargeForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    Shop_Form = ShopForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    Product_Form = ProductForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    Delete_Form = DeleteForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    Modify_Form = ModifyForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    

    # print("order_sid:", OrderCalcPrice_Form.order_sid.data)
    # print("order_calc_price_submit:", OrderCalcPrice_Form.order_calc_price_submit.data)
    # print("Order_Form.order_submit:", Order_Form.order_submit.data)
    
    # print("CancelShopOrder_Form.searchShopOrder_Cancel_submit:", CancelShopOrder_Form.searchShopOrder_Cancel_submit.data)
    # print("DoneShopOrder_Form.searchShopOrder_Done_submit:", DoneShopOrder_Form.searchShopOrder_Done_submit.data)

    # print("[308] Recharge_Form.recharge_addvalue:", Recharge_Form.recharge_addvalue)
    # print("[309] Order_Form.productNum:", Order_Form.productNum)
    # print("[310] Recharge_Form.recharge_submit.data:", Recharge_Form.recharge_submit.data)

    if CancelMyOrder_Form.searchMyOrder_Cancel_submit.data and CancelMyOrder_Form.validate():
        return cancelmyorder(CancelMyOrder_Form, searchShops, Shop_Form, Product_Form, searchMyOrder0, searchMyOrder1, searchMyOrder2, searchMyOrder3, searchShopOrder0, searchShopOrder1, searchShopOrder2, searchShopOrder3, searchTransactionRecord0, searchTransactionRecord1, searchTransactionRecord2, searchTransactionRecord3, Location_Form, Recharge_Form)
    elif CancelShopOrder_Form.searchShopOrder_Cancel_submit.data and CancelShopOrder_Form.validate():
        return cancelshoporder(CancelShopOrder_Form, searchShops, Shop_Form, Product_Form, searchMyOrder0, searchMyOrder1, searchMyOrder2, searchMyOrder3, searchShopOrder0, searchShopOrder1, searchShopOrder2, searchShopOrder3, searchTransactionRecord0, searchTransactionRecord1, searchTransactionRecord2, searchTransactionRecord3, Location_Form, Recharge_Form)
    elif DoneShopOrder_Form.searchShopOrder_Done_submit.data and DoneShopOrder_Form.validate():
        return doneshoporder(DoneShopOrder_Form, searchShops, Shop_Form, Product_Form, searchMyOrder0, searchMyOrder1, searchMyOrder2, searchMyOrder3, searchShopOrder0, searchShopOrder1, searchShopOrder2, searchShopOrder3, searchTransactionRecord0, searchTransactionRecord1, searchTransactionRecord2, searchTransactionRecord3, Location_Form, Recharge_Form)
    elif Order_Form.order_submit.data and Order_Form.validate():
        return order(Order_Form, searchShops, Shop_Form, Product_Form, searchMyOrder0, searchMyOrder1, searchMyOrder2, searchMyOrder3, searchShopOrder0, searchShopOrder1, searchShopOrder2, searchShopOrder3, searchTransactionRecord0, searchTransactionRecord1, searchTransactionRecord2, searchTransactionRecord3, Location_Form, Recharge_Form)
    elif Location_Form.location_submit.data and Location_Form.validate():
        return location_modify(Location_Form, searchShops, Shop_Form, Product_Form, searchMyOrder0, searchMyOrder1, searchMyOrder2, searchMyOrder3, searchShopOrder0, searchShopOrder1, searchShopOrder2, searchShopOrder3, searchTransactionRecord0, searchTransactionRecord1, searchTransactionRecord2, searchTransactionRecord3, Recharge_Form)
    elif Recharge_Form.recharge_submit.data and Recharge_Form.validate():
        return recharge(Recharge_Form, searchShops, Shop_Form, Product_Form, searchMyOrder0, searchMyOrder1, searchMyOrder2, searchMyOrder3, searchShopOrder0, searchShopOrder1, searchShopOrder2, searchShopOrder3, searchTransactionRecord0, searchTransactionRecord1, searchTransactionRecord2, searchTransactionRecord3, Location_Form)
    elif Shop_Form.Register_submit.data and Shop_Form.validate():
        return shop_register(searchShops, Shop_Form, Product_Form, searchMyOrder0, searchMyOrder1, searchMyOrder2, searchMyOrder3, searchShopOrder0, searchShopOrder1, searchShopOrder2, searchShopOrder3, searchTransactionRecord0, searchTransactionRecord1, searchTransactionRecord2, searchTransactionRecord3, Location_Form, Recharge_Form)
    elif Product_Form.Add_submit.data and Product_Form.validate():
        return product_add(searchShops, Shop_Form, Product_Form, searchMyOrder0, searchMyOrder1, searchMyOrder2, searchMyOrder3, searchShopOrder0, searchShopOrder1, searchShopOrder2, searchShopOrder3, searchTransactionRecord0, searchTransactionRecord1, searchTransactionRecord2, searchTransactionRecord3, Location_Form, Recharge_Form)
    elif Delete_Form.Delete_submit.data and Delete_Form.validate():
        return product_delete(Delete_Form, searchShops, Shop_Form, Product_Form, searchMyOrder0, searchMyOrder1, searchMyOrder2, searchMyOrder3, searchShopOrder0, searchShopOrder1, searchShopOrder2, searchShopOrder3, searchTransactionRecord0, searchTransactionRecord1, searchTransactionRecord2, searchTransactionRecord3, Location_Form, Recharge_Form)
    elif Modify_Form.Modify_submit.data and Modify_Form.validate():
        return product_modify(Modify_Form, searchShops, Shop_Form, Product_Form, searchMyOrder0, searchMyOrder1, searchMyOrder2, searchMyOrder3, searchShopOrder0, searchShopOrder1, searchShopOrder2, searchShopOrder3, searchTransactionRecord0, searchTransactionRecord1, searchTransactionRecord2, searchTransactionRecord3, Location_Form, Recharge_Form)

# , searchShops, Shop_Form, Product_Form, searchMyOrder0, searchMyOrder1, searchMyOrder2, searchMyOrder3, searchShopOrder0, searchShopOrder1, searchShopOrder2, searchShopOrder3, searchTransactionRecord0, searchTransactionRecord1, searchTransactionRecord2, searchTransactionRecord3

    return render_template(
                            "nav.html", 
                            # old version is outerjoin in next line
                            shop_product = Shop.query.join(Product, Shop.sid == Product.sid and Shop.pid == current_user.get_id()).add_columns(Product.name, Product.pid, Product.price, Product.quantity, Product.picture),
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

@website.route('/', methods = ['GET','POST'])
@login_required
def home():
    print("home called default status = 3")
    return homee(0)


def searchshop_():
    #initianl searchShops
    searchShops = Shop.query.all()

    shop = request.args.get('shopname')
    meal = request.args.get('meal')
    category = request.args.get('category')

    searchShops = shop_comp(shop, searchShops)
    searchShops = meal_comp(meal, searchShops)
    searchShops = cate_comp(category, searchShops)

    # print("[120] searchshops:", searchShops)

    # distance
    # print(type(User.query.all()), User.query.all())
    # print(User.query.filter_by(id=current_user.get_id()).first(), User.query.filter_by(id=current_user.get_id()).all(), User.query.filter_by(id=current_user.get_id()))
    # print("[187] type ", type(request.args.get('distance')), request.args.get('distance'))
    if str(type(request.args.get('distance'))) == "<class 'str'>":
        distanceL, distanceU = distance_range(request.args.get('distance'))
        remove_list = []
        # points = [(x.latitude, x.longitude) for x in searchShops] # Shop.query.all() for all shop
        for x in searchShops:
            lat = x.latitude
            lon = x.longitude
            dis = haversine(lat, lon, User.query.filter_by(id=current_user.get_id()).all()[0].latitude, User.query.filter_by(id=current_user.get_id()).all()[0].longitude)
            if(dis < distanceL or dis >= distanceU):
                remove_list.append(x)
        for x in remove_list:
            searchShops.remove(x)

    for x in searchShops:
        lat = x.latitude
        lon = x.longitude
        dis = haversine(lat, lon, User.query.filter_by(id=current_user.get_id()).all()[0].latitude, User.query.filter_by(id=current_user.get_id()).all()[0].longitude)
        x.distance = distance_level(dis)
        x.deliveryFee = max(10, round(dis*0.01))

    # price
    priceL = request.args.get('priceL')
    priceU = request.args.get('priceU')
    if(str(type(request.args.get('priceL'))) == "<class 'str'>" and priceL != ""):
        if(priceL.isnumeric()):
            priceL = int(priceL)
        else:
            priceL = 1e51
    else:
        priceL = 0
    if(str(type(request.args.get('priceU'))) == "<class 'str'>" and priceU != ""):
        if(priceU.isnumeric()):
            priceU = int(priceU)
        else:
            priceU = -1
    else:
        priceU = 1e50

    if((str(type(priceL)) == "<class 'int'>" or str(type(priceL)) == "<class 'float'>") and (str(type(priceU)) == "<class 'int'>" or str(type(priceU)) == "<class 'float'>")):
        allow_list = []
        all_product = Product.query.all()
        # print('[162] allproduct:', all_product)
        for x in all_product:
            if(priceL <= x.price and x.price <= priceU):
                allow_list.append(x.sid)
            
        # print("[167] allow_list:", allow_list)
        # print("[168] searchshops:", searchShops)

        i = 0
        while(i < len(searchShops)):
            if((searchShops[i].sid not in allow_list)):
                searchShops.remove(searchShops[i])
                continue
            i += 1
        
        # print("[177] searchshops:", searchShops)

    all_product = Product.query.all()
    for y in searchShops:
        y.products = []
    
    for x in all_product:
        for y in searchShops:
            if(y.sid == x.sid):
                y.products.append(x)

    # for y in searchShops:
    #     print("[191] itme in searchShops", y)
    
    # print("[186] all:", Shop.query.all())
    # print("[270] searchShops:", searchShops.pro)
    for _ in range(len(searchShops)):
        # print("[191] vars:", vars(searchShops[_]))
        searchShops[_].ID = _ + 1

    return searchShops


@website.route('/#myorder', methods = ['GET','POST'])
@login_required
def myorder():

    Shop_Form = ShopForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    Product_Form = ProductForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    Location_Form = LocationForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    Recharge_Form = RechargeForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack

    searchShops = searchshop_()
    searchMyOrder0, searchMyOrder1, searchMyOrder2, searchMyOrder3 = searchmyorder()
    searchShopOrder0, searchShopOrder1, searchShopOrder2, searchShopOrder3 = searchshoporder()
    searchTransactionRecord0, searchTransactionRecord1, searchTransactionRecord2, searchTransactionRecord3 = searchtransactionrecord()

    return render_template(
                            "nav.html", 
                            # old version is outerjoin in next line
                            shop_product = Shop.query.join(Product, Shop.sid == Product.sid and Shop.pid == current_user.get_id()).add_columns(Product.name, Product.pid, Product.price, Product.quantity, Product.picture),
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

@website.route('/get-status', methods = ['POST'])
def getStatus():
    information = request.data.decode()
    print("get status called")
    print(information)
    # return big_string(homee(information),25,2)
    # return homee()
    return "I don't know what to return! QAQ"
    # return redirect('/?status=' + information)


def big_string(s, a, b):
    return ''.join(s.split('\n')[a:-b])
    