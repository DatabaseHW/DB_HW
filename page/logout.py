from flask import *
from flask_login import *

from configuration import website
from forms import LoginForm
from model.user import User
from page.login import direct_login



@website.route('/logout')  
@login_required
def logout():
    logout_user()  
    return redirect(url_for('direct_login'))