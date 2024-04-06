from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from cryptography.fernet import Fernet

app = Flask(__name__)

client = MongoClient('localhost', 27017) #, username='jdwilcox32', password='jfolA6tcIb9k9HXy'

db = client.flask_db
logins = db.logins

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method=='POST':
        #key=Fernet.generate_key() -- GIVE USER A KEY ON ACCOUNT CREATION
        user_key = request.form['user_key']
        login_website = request.form['login_website']
        login_username = request.form['login_username']
        login_password = request.form['login_password']
        key=user_key
        k=Fernet(key)
        logins.insert_one({'login_website': k.encrypt(bytes(login_website,'utf-8')), 'login_username': k.encrypt(bytes(login_username,'utf-8')), 'login_password': k.encrypt(bytes(login_password,'utf-8'))})
        return redirect(url_for('index'))

    all_logins = logins.find()
    return render_template('index.html', logins=all_logins)

@app.post('/<id>/delete/')
def delete(id):
    logins.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

# @app.post('/<key>/decrypt')
# def decrypt(key):
#     logins.
#     return redirect(url_for('index'))