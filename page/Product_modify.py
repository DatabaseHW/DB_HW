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

def product_modify(Shop_Form, Product_Form, Modify_Form):
    delete_product = Product.query.filter_by(pid = Modify_Form.modify_pid.data).first()
    new_product = Product(delete_product.sid, delete_product.name, Modify_Form.quantity_modify.data, Modify_Form.price_modify.data, delete_product.picture)

    user_database.session.delete(delete_product)
    user_database.session.add(new_product)
    user_database.session.commit()
    flash("修改成功",category="product modify success")
    return render_template(
                            "nav.html", 
                            shop_product = Shop.query.join(Product, Shop.sid == Product.sid and Shop.pid == current_user.get_id()).add_columns(Product.name, Product.pid, Product.price, Product.quantity, Product.picture),
                            shop_form = Shop_Form, 
                            product_form = Product_Form,
                            user = User.query.filter_by(id=current_user.get_id()).first(), 
                            has_shop=Shop.query.filter_by(uid=current_user.get_id())
                        )
