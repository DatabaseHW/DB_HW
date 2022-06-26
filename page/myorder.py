# import base64
# from fileinput import filename
# from uuid import UUID
# from flask import *
# from flask_login import *
# from numpy import require
# from flask_sqlalchemy import *

# from configuration import website, user_database
# from forms import RechargeForm
# from model.shop import Shop
# from model.user import User
# from model.product import Product

# def myorder(Shop_Form, Product_Form, MyOrder_Form, searchShops):
    
#     print("hello, this is my order")


#     # TODO error message: can not be float
#     flash("加值成功",category="recharge success")
#     return render_template(
#                             "nav.html", 
#                             user = User.query.filter_by(id=current_user.get_id()).first(), 
#                             searchShops = searchShops, 
#                             shop_form = Shop_Form,
#                             product_form = Product_Form,
#                             has_shop=Shop.query.filter_by(uid=current_user.get_id())
#                         )
