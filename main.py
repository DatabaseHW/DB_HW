from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os



import page.login
import page.home
import page.register
import page.logout
from configuration import website, user_database

if __name__ == '__main__':
    # user_database.drop_all()    # 希望程式重啟資料庫不會被刪除，就把這行註解
    user_database.create_all()
    website.run(host="0.0.0.0", port=5000)