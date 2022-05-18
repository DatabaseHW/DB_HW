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
from page.shop_register import shop_register


@website.route('/',methods = ['GET','POST'])
@login_required
def home():
    Shop_Form = ShopForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    Product_Form = ProductForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    if Shop_Form.Register_submit.data and Shop_Form.validate():
        return shop_register(Shop_Form, Product_Form)
    elif Product_Form.Add_submit.data and Product_Form.validate():
        selling_shop = Shop.query.filter_by(uid = current_user.get_id(), name = Product_Form.shop_name.data).first()

        if selling_shop is None:
            flash("商店不存在", category="Product add errors")
            return render_template(
                                    'nav.html', 
                                    shop_product_form = Shop.query.join(Shop, Shop.sid == Product.sid and Shop.pid == current_user.get_id()).add_columns(Product.name, Product.pid, Product.price, Product.quantity, Product.picture),
                                    shop_form = Shop_Form, 
                                    name_repeated=True, 
                                    user = User.query.filter_by(id=current_user.get_id()).first(), 
                                    has_shop=Shop.query.filter_by(uid=current_user.get_id())
                                )
        product = Product.query.filter_by(name=Product_Form.name.data, sid = selling_shop.sid).first()
        if product is not None:
            flash("商品已經存在", category="Product add errors")
            return render_template(
                                    'nav.html', 
                                    shop_product_form = Shop.query.join(Shop, Shop.sid == Product.sid and Shop.pid == current_user.get_id()).add_columns(Product.name, Product.pid, Product.price, Product.quantity, Product.picture),
                                    shop_form = Shop_Form, 
                                    name_repeated=True, 
                                    user = User.query.filter_by(id=current_user.get_id()).first(), 
                                    has_shop=Shop.query.filter_by(uid=current_user.get_id())
                                )
        else:
            images = base64.b64encode(request.files['picture'].read()).decode('ascii')
            new_product = Product(selling_shop.sid, Product_Form.name.data, Product_Form.quantity.data, Product_Form.price.data, images)
            user_database.session.add(new_product)
            user_database.session.commit()
            flash("新增成功",category="product add success")
            return render_template(
                                    'nav.html', 
                                    shop_product_form = Shop.query.join(Shop, Shop.sid == Product.sid and Shop.pid == current_user.get_id()).add_columns(Product.name, Product.pid, Product.price, Product.quantity, Product.picture),
                                    shop_form = Shop_Form, 
                                    name_repeated=False, 
                                    user = User.query.filter_by(id=current_user.get_id()).first(), 
                                    has_shop=Shop.query.filter_by(uid=current_user.get_id())
                                )

    return render_template(
                            "nav.html", 
                            shop_product_form = Shop.query.join(Shop, Shop.sid == Product.sid and Shop.pid == current_user.get_id()).add_columns(Product.name, Product.pid, Product.price, Product.quantity, Product.picture),
                            shop_form = Shop_Form, 
                            name_repeated=False, 
                            user = User.query.filter_by(id=current_user.get_id()).first(), 
                            has_shop=Shop.query.filter_by(uid=current_user.get_id())
                        )
