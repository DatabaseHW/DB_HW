from flask import *
from flask_login import *

from configuration import website
from forms import LoginForm
from model.user import User

@website.route("/login", methods = ['GET','POST'])
def direct_login():
    Login_form = LoginForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    
    # if Login_form.validate_on_submit():
    #     user = User.query.filter_by(account=Login_form.account.data).first()
    #     if user is not None:
    #         login_user(user)
    #         return redirect(url_for('home'))

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if Login_form.validate_on_submit():
        user = User.query.filter_by(account=Login_form.account.data).first()
        if user is not None and user.check_password(Login_form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("帳號 or 密碼有錯",category="wrong_passwd_or_account")
            return render_template('index.html', form = Login_form)
    else:
        return render_template('index.html', form = Login_form)