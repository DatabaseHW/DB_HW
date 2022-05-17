from uuid import UUID
from flask import *
from flask_login import LoginManager, login_url, login_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os

from configuration import website


@website.route('/')
def home():
    return render_template("nav.html")
