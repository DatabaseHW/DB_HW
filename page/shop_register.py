from uuid import UUID
from flask import *
from flask_login import *
from numpy import require


from configuration import website, user_database
from forms import LoginForm, ShopForm, ProductForm
from model.shop import Shop
from model.user import User
from model.product import Product

def shop_register(searchShops, shop_product, Shop_Form, Product_Form, searchMyOrder0, searchMyOrder1, searchMyOrder2, searchMyOrder3, searchShopOrder0, searchShopOrder1, searchShopOrder2, searchShopOrder3, searchTransactionRecord0, searchTransactionRecord1, searchTransactionRecord2, searchTransactionRecord3, Location_Form, Recharge_Form):
    shop = Shop.query.filter_by(name=Shop_Form.name.data).first()
    if shop is not None:
        flash("商店名稱不可重複",category="name_repeated")
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
    else:
        new_shop = Shop(current_user.get_id(), Shop_Form.name.data, Shop_Form.latitude.data, Shop_Form.longitude.data, Shop_Form.categorys.data)
        user_database.session.add(new_shop)
        user_database.session.commit()
        flash("商店註冊成功",category="register success")
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