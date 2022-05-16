from flask import *
import os

website = Flask(__name__)
website.secret_key = os.urandom(16).hex()

@website.route('/')
def home():
    return render_template("nav.html")

@website.route("/login", methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form['user']
        return redirect(url_for('home'))
    else:
        return render_template("index.html",)

if __name__ == '__main__':
    website.run()