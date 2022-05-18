from flask import *
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_url, login_user
import os 

html_folder_path = os.path.join(os.path.dirname(__file__),'path_html')

#website configuration
website = Flask(__name__)

website.secret_key = os.urandom(16).hex()
basedir = os.path.abspath(__file__)
website.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost:3306/dbproject"


# Login page configuration
user_database = SQLAlchemy(website)
user_migrate = Migrate(website, user_database)

Login_manager = LoginManager()
Login_manager.init_app(website)
Login_manager.login_view = 'direct_login'