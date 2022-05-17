from uuid import UUID
from flask import *
from flask_login import LoginManager, login_url, login_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from configuration import website
from forms import LoginForm
from model.user import User

@website.route("/login", methods = ['GET','POST'])
def direct_login():
    Login_form = LoginForm(request.form, meta={'csrf': False})  # may be attacked by csrf attack
    
    if Login_form.validate_on_submit():
        user = User.query.filter_by(account=Login_form.account.data).first()
        if user is not None and user.check_password(Login_form.password.data) :
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("帳號 or 密碼有錯")
            return render_template('index.html', form = Login_form)
    else:
        return render_template('index.html', form = Login_form)