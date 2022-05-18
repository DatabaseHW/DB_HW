from uuid import UUID
from flask import *
from flask_login import *
from numpy import require


from configuration import website, user_database
from forms import LoginForm, ShopForm
from model.shop import Shop
from model.user import User


@website.route('/',methods = ['GET','POST'])
@login_required
def home():
    Shop_Form = ShopForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    if Shop_Form.Register_submit.data and Shop_Form.validate():
        shop = Shop.query.filter_by(name=Shop_Form.name.data).first()
        if shop is not None:
            return render_template('nav.html', name_repeated=True, has_shop=None, user = User.query.filter_by(id=current_user.get_id()).first())
        else:
            new_shop = Shop(current_user.get_id(), Shop_Form.name.data,Shop_Form.latitude.data,Shop_Form.longitude.data,Shop_Form.categorys.data)
            user_database.session.add(new_shop)
            user_database.session.commit()
            return render_template('nav.html', name_repeated=False, user = User.query.filter_by(id=current_user.get_id()).first(), has_shop=new_shop)

    return render_template("nav.html", name_repeated=False, user = User.query.filter_by(id=current_user.get_id()).first(), has_shop=Shop.query.filter_by(uid=current_user.get_id()))