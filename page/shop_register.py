from uuid import UUID
from flask import *
from flask_login import *
from numpy import require


from configuration import website, user_database
from forms import LoginForm, ShopForm, ProductForm
from model.shop import Shop
from model.user import User
from model.product import Product

def shop_register(Shop_Form, Product_Form):
    shop = Shop.query.filter_by(name=Shop_Form.name.data).first()
    if shop is not None:
        flash("商店名稱不可重複",category="name_repeated")
        return render_template(
                                    'nav.html', 
                                    shop_product = Shop.query.join(Product, Shop.sid == Product.sid and Shop.pid == current_user.get_id()).add_columns(Product.name, Product.pid, Product.price, Product.quantity, Product.picture),
                                    shop_form = Shop_Form, 
                                    product_form = Product_Form,
                                    user = User.query.filter_by(id=current_user.get_id()).first(), 
                                    has_shop=Shop.query.filter_by(uid=current_user.get_id())
                                )
    else:
        new_shop = Shop(current_user.get_id(), Shop_Form.name.data, Shop_Form.latitude.data, Shop_Form.longitude.data, Shop_Form.categorys.data)
        user_database.session.add(new_shop)
        user_database.session.commit()
        flash("商店註冊成功",category="register success")
        return render_template(
                                    'nav.html', 
                                    shop_product = Shop.query.join(Product, Shop.sid == Product.sid and Shop.pid == current_user.get_id()).add_columns(Product.name, Product.pid, Product.price, Product.quantity, Product.picture),
                                    shop_form = Shop_Form, 
                                    product_form = Product_Form,
                                    user = User.query.filter_by(id=current_user.get_id()).first(), 
                                    has_shop=Shop.query.filter_by(uid=current_user.get_id())
                                )