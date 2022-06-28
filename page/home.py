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
import bcrypt
from flask_bcrypt import Bcrypt
from page.order import order
# from page.myorder import myorder
# from page.orderCalcPrice import orderCalcPrice
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

def searchmyorder(status):
    searchMyOrder = Order.query.all()
    i = 0
    while(i < len(searchMyOrder)):
        if((searchMyOrder[i].uid != current_user.get_id())):
            searchMyOrder.remove(searchMyOrder[i])
            continue
        i += 1
    
    all_items = Item.query.all()
    for i in range(len(searchMyOrder)):
        searchMyOrder[i].products = []
        for y in all_items:
            if searchMyOrder[i].oid == y.oid:
                prod = Product.query.filter_by(pid=y.pid).first()
                new_product = Product(prod.sid, prod.name, y.quantity, prod.price, prod.picture, prod.pid)
                searchMyOrder[i].products.append(new_product)
                # print("[135] searchMyOrder[", i, "].products:", searchMyOrder[i].products)


    searchMyOrder0 = []
    searchMyOrder1 = []
    searchMyOrder2 = []
    searchMyOrder3 = []
    for x in searchMyOrder:
        searchMyOrder0.append(x)
        searchMyOrder1.append(x)
        searchMyOrder2.append(x)
        searchMyOrder3.append(x)

    # print(searchMyOrder0)

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
    
    # print("[147] num of searcMyOrder:", len(searchMyOrder))
    # print("[148] status:", type(status), status)
    
    for _ in range(len(searchMyOrder0)):
        searchMyOrder0[_].ID = _ + 1
    for _ in range(len(searchMyOrder1)):
        searchMyOrder1[_].ID = _ + 1
    for _ in range(len(searchMyOrder2)):
        searchMyOrder2[_].ID = _ + 1
    for _ in range(len(searchMyOrder3)):
        searchMyOrder3[_].ID = _ + 1

    print(len(searchMyOrder0), len(searchMyOrder1), len(searchMyOrder2), len(searchMyOrder3))
    return searchMyOrder0, searchMyOrder1, searchMyOrder2, searchMyOrder3


def searchshoporder(status):
    searchShopOrder = Order.query.all()
    sid = request.args.get('shopid')
    print("[158] sid:", sid)
    
    i = 0
    while(i < len(searchShopOrder)):
        if((searchShopOrder[i].uid != sid)):
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
        # print("[191] vars:", vars(searchShops[_]))
        searchShopOrder[_].ID = _ + 1

    # for x in searchShopOrder:
    #     print(x.products)
    # print("---------------------------------------")
    return searchShopOrder
    


@website.route('/<int:status>', methods = ['GET','POST'])
@login_required
def homee(status=3):
    print("homee called Status: ",type(status),status)
    try:
        status = int(status)
    except:
        status = int(status[1])
    db__ = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='dbproject', charset='utf8')
    cur = db__.cursor()
    # if request.args.get('shopname') == "" and request.args.get('category') == "" :
    #     sql = "SELECT * FROM shops"
    #     cur.execute(sql)
    # elif request.args.get('category') == "" :
    #     sql = "SELECT * FROM shops WHERE name=%s"
    #     cur.execute(sql, (str(request.args.get('shopname'))))
    # elif request.args.get('shopname') == "" :
    #     sql = "SELECT * FROM shops WHERE categorys=%s"
    #     cur.execute(sql, (request.args.get('category')))
    # else :
    #     sql = "SELECT * FROM shops WHERE name=%s and categorys=%s"
    #     cur.execute(sql, (request.args.get('shopname'), request.args.get('category')))
    
    # sql = "SELECT * FROM shops"
    # cur.execute(sql)
    # searchShops = [Shop(_[0], _[2], _[3], _[4], _[5], _[1]) for _ in list(cur.fetchall())]
    
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

    # my order list
    # OrderCalcPrice_Form = OrderCalcPriceForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    # MyOrder_Form = MyOrderForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
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
    
    # print("MyOrder_Form.my_order_submit.data:", MyOrder_Form.my_order_submit.data)

    # print("order_sid:", OrderCalcPrice_Form.order_sid.data)
    # print("order_calc_price_submit:", OrderCalcPrice_Form.order_calc_price_submit.data)
    # print("Order_Form.order_submit:", Order_Form.order_submit.data)
    
    # print("CancelMyOrder_Form.searchMyOrder_Cancel_submit:", CancelMyOrder_Form.searchMyOrder_Cancel_submit.data)
    # print("CancelShopOrder_Form.searchShopOrder_Cancel_submit:", CancelShopOrder_Form.searchShopOrder_Cancel_submit.data)
    # print("DoneShopOrder_Form.searchShopOrder_Done_submit:", DoneShopOrder_Form.searchShopOrder_Done_submit.data)

    # if MyOrder_Form.my_order_submit.data:
    #     return myorder(Shop_Form, Product_Form, MyOrder_Form, searchShops)
    # print("[308] Recharge_Form.recharge_addvalue:", Recharge_Form.recharge_addvalue)
    # print("[309] Order_Form.productNum:", Order_Form.productNum)
    # print("[310] Recharge_Form.recharge_submit.data:", Recharge_Form.recharge_submit.data)

    if CancelMyOrder_Form.searchMyOrder_Cancel_submit.data and CancelMyOrder_Form.validate():
        return cancelmyorder(Shop_Form, Product_Form, CancelMyOrder_Form, searchShops)
    elif CancelShopOrder_Form.searchShopOrder_Cancel_submit.data and CancelShopOrder_Form.validate():
        return cancelshoporder(Shop_Form, Product_Form, CancelShopOrder_Form, searchShops)
    elif DoneShopOrder_Form.searchShopOrder_Done_submit.data and DoneShopOrder_Form.validate():
        return doneshoporder(Shop_Form, Product_Form, DoneShopOrder_Form, searchShops)
    elif Order_Form.order_submit.data and Order_Form.validate():
        return order(Shop_Form, Product_Form, Order_Form, searchShops)
    elif Location_Form.location_submit.data and Location_Form.validate():
        return location_modify(Shop_Form, Product_Form, Location_Form, searchShops)
    elif Recharge_Form.recharge_submit.data and Recharge_Form.validate():
        return recharge(Shop_Form, Product_Form, Recharge_Form, searchShops)
    elif Shop_Form.Register_submit.data and Shop_Form.validate():
        return shop_register(Shop_Form, Product_Form)
    elif Product_Form.Add_submit.data and Product_Form.validate():
        return product_add(Shop_Form, Product_Form)
    elif Delete_Form.Delete_submit.data and Delete_Form.validate():
        return product_delete(Shop_Form, Product_Form, Delete_Form)
    elif Modify_Form.Modify_submit.data and Modify_Form.validate():
        return product_modify(Shop_Form, Product_Form, Modify_Form)

    #search my order
    searchMyOrder0, searchMyOrder2, searchMyOrder1, searchMyOrder3 = searchmyorder(status)
    searchShopOrders = searchshoporder(status)
    # print("[352] searchMyOrders", searchMyOrders)
    # for x in searchMyOrders:
    #     print(x.products)
    
    return render_template(
                            "nav.html", 
                            # old version is outerjoin in next line
                            shop_product = Shop.query.join(Product, Shop.sid == Product.sid and Shop.pid == current_user.get_id()).add_columns(Product.name, Product.pid, Product.price, Product.quantity, Product.picture),
                            searchShops = searchShops, 
                            shop_form = Shop_Form, 
                            product_form = Product_Form,
                            user = User.query.filter_by(id=current_user.get_id()).first(), 
                            has_shop=Shop.query.filter_by(uid=current_user.get_id()),
                            searchMyOrders = searchMyOrder0,
                            searchShopOrders = searchShopOrders
                        )

@website.route('/', methods = ['GET','POST'])
@login_required
def home():
    print("home called default status = 3")
    return homee(0)


@website.route('/#myorder', methods = ['GET','POST'])
@login_required
def myorder():
    print("haha")
    searchMyOrder = Order.query.all()
    print("searchMyOrder:", searchMyOrder)

    return render_template(
                            "nav.html", 
                            # old version is outerjoin in next line
                            shop_product = Shop.query.join(Product, Shop.sid == Product.sid and Shop.pid == current_user.get_id()).add_columns(Product.name, Product.pid, Product.price, Product.quantity, Product.picture),
                            # searchShops = searchShops,
                            # shop_form = Shop_Form,
                            # product_form = Product_Form,
                            user = User.query.filter_by(id=current_user.get_id()).first(), 
                            has_shop=Shop.query.filter_by(uid=current_user.get_id()),
                            searchMyOrders = [Order("1","1","1","1","1","1","1","1")]
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
    