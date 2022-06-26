# import base64
# from fileinput import filename
# from uuid import UUID
# from flask import *
# from flask_login import *
# from numpy import require
# from flask_sqlalchemy import *

# from configuration import website, user_database
# from forms import OrderCalcPriceForm
# from model.shop import Shop
# from model.user import User
# from model.product import Product
# from model.order import Order

# def orderCalcPrice(Shop_Form, Product_Form, searchShops, OrderCalcPrice_Form):
#     # TODO: edit this file
#     print("hahah calc price")
#     order_sid = OrderCalcPrice_Form.order_sid.data

#     orderProducts = []
#     all_product = Product.query.all()
#     print("order_sid:", order_sid) # always = None
#     for x in all_product:
#         if(x.sid == order_sid):
#             productNum = request.args.get('productNum' + x.pid)
#             print("product num:", productNum)
#             # print(productNum)
#             orderProducts.append(Product(x.sid, x.name, productNum, x.price, x.picture, x.pid))
    
#     print("orderprouducts:", orderProducts)

#     # flash("加值成功",category="order price calculate success")
#     # i don't wnat to refresh the home page, so that the order model in html can show properly
#     # or, can we process "calculate price" in JavaScript ?
#     return render_template(
#                             "nav.html", 
#                             user = User.query.filter_by(id=current_user.get_id()).first(), 
#                             searchShops = searchShops, 
#                             shop_form = Shop_Form,
#                             product_form = Product_Form,
#                             has_shop=Shop.query.filter_by(uid=current_user.get_id())
#                         )
