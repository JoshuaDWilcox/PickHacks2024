from flask import Flask, render_template, request, url_for, redirect, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from cryptography.fernet import Fernet
from pymongo.server_api import ServerApi

app = Flask(__name__)
app.secret_key = b'SECRETjojn2r982h2j@J$O#@$J@jo@#'

client = MongoClient('mongodb+srv://jdwilcox32:<password>@cluster0.f9nwtyt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0', server_api=ServerApi('1'), username='jdwilcox32', password='jfolA6tcIb9k9HXy') #, username='jdwilcox32', password='jfolA6tcIb9k9HXy'
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.flask_db
logins = db.logins

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method=='POST':
        try:
            #key=Fernet.generate_key() -- GIVE USER A KEY ON ACCOUNT CREATION
            user_key = request.form['user_key']
            login_website = request.form['login_website']
            login_username = request.form['login_username']
            login_password = request.form['login_password']
            key=user_key
            k=Fernet(key)
            logins.insert_one({'login_website': login_website, 'login_username': k.encrypt(bytes(login_username,'utf-8')), 'login_password': k.encrypt(bytes(login_password,'utf-8'))})
        except:
            flash("Error! Please try again")
        return redirect(url_for('index'))

    all_logins = logins.find()
    return render_template('index.html', logins=all_logins)


@app.post('/<id>/delete/')
def delete(id):
    logins.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

@app.post('/<id>/decrypt')
def decrypt(id):
    return redirect(url_for('decryption',decrypt_id=id))

@app.route('/decryption/<decrypt_id>',methods=('GET','POST'))
def decryption(decrypt_id):
    decrypt_login = logins.find_one({"_id": ObjectId(decrypt_id)})
    flash("Website: "+decrypt_login["login_website"])
    if request.method=='POST':
        try:
            user_key = request.form['user_key']
            k=Fernet(user_key)
            flash("Username: "+k.decrypt(decrypt_login["login_username"]).decode("utf-8")+"  ")
            flash("Password: "+k.decrypt(decrypt_login["login_password"]).decode("utf-8")+"  ")
            return render_template('decryption.html',id=decrypt_id)
        except:
            flash("Username: ******")
            flash("Password: ******")
            flash("Improper key. Please try again.")
            return render_template('decryption.html',id=decrypt_id)

    flash("Username: ******")
    flash("Password: ******")
    return render_template('decryption.html',id=decrypt_id)

