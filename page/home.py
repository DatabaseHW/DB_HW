from uuid import UUID
from flask import *
from flask_login import *


from configuration import website


@website.route('/')
@login_required
def home():
    return render_template("nav.html")
