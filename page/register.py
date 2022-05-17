from nturl2path import url2pathname
from flask import *

from model.user import User
from configuration import user_database, website
from forms import RegisterForm

@website.route("/sign-up", methods = ['GET','POST'])
def Register():
    Sign_form = RegisterForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    if Sign_form.validate_on_submit():
        user = User.query.filter_by(account=Sign_form.account.data).first()
        if user is not None:
            flash("帳號已被註冊")
            return render_template('sign-up.html', form = Sign_form)
        else:
            new_user = User(Sign_form.account.data,Sign_form.password.data,Sign_form.name.data,Sign_form.phonenumber.data,Sign_form.latitude.data,Sign_form.longitude.data)
            user_database.session.add(new_user)
            user_database.session.commit()
            return redirect(url_for('direct_login'))
            
    else:
        return render_template('sign-up.html', form = Sign_form)