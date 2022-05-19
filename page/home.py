import base64
from fileinput import filename
from uuid import UUID
from flask import *
from flask_login import *
from numpy import require
from flask_sqlalchemy import *

from configuration import website, user_database
from forms import LoginForm, ModifyForm, ShopForm, ProductForm, DeleteForm
from model.shop import Shop
from model.user import User
from model.product import Product
from page.shop_register import shop_register
from page.Product_add import product_add
from page.Product_delete import product_delete
from page.Product_modify import product_modify

@website.route('/',methods = ['GET','POST'])
@login_required
def home():
    Shop_Form = ShopForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    Product_Form = ProductForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    Delete_Form = DeleteForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    Modify_Form = ModifyForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    if Shop_Form.Register_submit.data and Shop_Form.validate():
        return shop_register(Shop_Form, Product_Form)
    elif Product_Form.Add_submit.data and Product_Form.validate():
       return product_add(Shop_Form, Product_Form)
    elif Delete_Form.Delete_submit.data and Delete_Form.validate():
        return product_delete(Shop_Form, Product_Form, Delete_Form)
    elif Modify_Form.Modify_submit.data and Modify_Form.validate():
        return product_modify(Shop_Form, Product_Form, Modify_Form)
    
    return render_template(
                            "nav.html", 
                            shop_product = Shop.query.join(Product, Shop.sid == Product.sid and Shop.pid == current_user.get_id()).add_columns(Product.name, Product.pid, Product.price, Product.quantity, Product.picture),
                            shop_form = Shop_Form, 
                            product_form = Product_Form,
                            user = User.query.filter_by(id=current_user.get_id()).first(), 
                            has_shop=Shop.query.filter_by(uid=current_user.get_id())
                        )
