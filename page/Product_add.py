import base64
from fileinput import filename
from uuid import UUID
from flask import *
from flask_login import *
from numpy import require
from flask_sqlalchemy import *

from configuration import website, user_database
from forms import LoginForm, ShopForm, ProductForm
from model.shop import Shop
from model.user import User
from model.product import Product
 
 
def product_add(searchShops, Shop_Form, Product_Form, searchMyOrder0, searchMyOrder1, searchMyOrder2, searchMyOrder3, searchShopOrder0, searchShopOrder1, searchShopOrder2, searchShopOrder3, searchTransactionRecord0, searchTransactionRecord1, searchTransactionRecord2, searchTransactionRecord3, Location_Form, Recharge_Form):
    selling_shop = Shop.query.filter_by(uid = current_user.get_id(), name = Product_Form.shop_name.data).first()

    if selling_shop is None:
        flash("商店不存在", category="product add errors")
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
    product = Product.query.filter_by(name=Product_Form.name.data, sid = selling_shop.sid).first()
    if product is not None:
        flash("商品已經存在", category="product add errors")
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
    else:
        images = base64.b64encode(request.files['picture'].read())
        new_product = Product(selling_shop.sid, Product_Form.name.data, Product_Form.quantity.data, Product_Form.price.data, images)
        user_database.session.add(new_product)
        user_database.session.commit()
        flash("商品新增成功",category="product add success")
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