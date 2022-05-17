from flask import *
import os
from flask_sqlalchemy import SQLAlchemy

def init():
    return

# TODO:
# return
#   UID : signup successfully as user of UID
#   -1  : ID overlap
def signupValidation(inputUserData):
    return 0

# TODO:
def dbAddUser(userData):
    return
    # TODO: 將以下 sql_cmd 字串寫入：insert a user with data be userData
    sql_cmd = """
        select *
        from user
        """
    query_data = db.engine.execute(sql_cmd)
    print("query_data:", query_data.fetchall())

# TODO:
# return
#   UID : login successfully as user of UID
#   -1  : no such ID
#   -2  : wrong PWD
def loginValidation(ID, PWD):
    return 0

# An example of interaction of flask with mysql db
def printAllUsers():
    sql_cmd = """
        select *
        from user
        """
    query_data = db.engine.execute(sql_cmd)
    print("query_data:", query_data.fetchall())

website = Flask(__name__)
website.secret_key = os.urandom(16).hex()

db = SQLAlchemy()
website.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost:3306/dbproject"
db.init_app(website)

@website.route('/')
def home():
    printAllUsers()
    if False:
    # TODO: fix this line
    # if session.get('UID') == None:
        redirect(url_for('login'))
    else:
        return render_template("nav.html")

@website.route("/login", methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        inputID = request.form['Account']
        inputPWD = request.form['Account']
        _UID = loginValidation(inputID, inputPWD)
        if _UID == -1:
            print("Wrong ID")
        elif _UID == -2:
            print("Wrong PWD")
        else:
            session['UID'] = _UID
            print("Login Successfully")
            print("UID:", _UID)
            return redirect(url_for('home'))
    return render_template("index.html")

@website.route("/signup", methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        inputName = request.form['Name']
        inputContact = request.form['Phonenumber']
        inputID = request.form['Account']
        inputPWD = request.form['Password']
        inputRePWD = request.form['Re-password']
        inputLatitude = request.form['Latitude']
        inputLongitude = request.form['Longitude']
        if inputPWD != inputRePWD:
            print("Password and retype password not match")
            return render_template("sign-up.html")
        inputUserData = {
            "Name": inputName, 
            "Contact": inputContact, 
            "ID": inputID, 
            "PWD": inputPWD, 
            "Latitude": inputLatitude, 
            "Longitude": inputLongitude, 
        }
        _UID = signupValidation(inputUserData)
        if _UID == -1:
            print("ID used by other")
        else:
            print("Sign-up successfully")
            dbAddUser(inputUserData)
            return redirect(url_for('login'))
            
    return render_template("sign-up.html")

if __name__ == '__main__':
    init()
    website.run()
