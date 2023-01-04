#projenin calisan ilk hali

from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response 
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
import bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from db import db
import random
import string
from functools import wraps
from models import User, Urls
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
                    #db configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secret-secret'
db.init_app(app)
                     #db start

                     #defining db elements
jwt = JWTManager(app)

                    #creating db table
"""@app.before_first_request
def create_tables():
    db.create_all() 
    db.init_app(app)"""
                    #short url choose and create function
def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        rand_letters = random.choices(letters, k=3)
        rand_letters = "".join(rand_letters)
        short_url = Urls.query.filter_by(short=rand_letters).first()
        if not short_url:
            return rand_letters
            
    
@app.route('/register', methods=['POST'])
def register():
    try:
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        
        if not email:
            return 'Missing email', 400
        if not password:
            return 'Missing password', 400
        
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user = User(email=email, hash=hashed)
        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity={"email": email})
        return {"access_token": access_token}, 200
    except IntegrityError:
        # the rollback func reverts the changes made to the db ( so if an error happens after we commited changes they will be reverted )
        db.session.rollback()
        return 'User Already Exists', 400
    except AttributeError:
        return 'Provide an Email and Password in JSON format in the request body', 400


@app.route('/login', methods=['POST'])
def login():
    
        email = request.json.get('email', None)
        password = request.json.get('password', None)
                
        user = User.query.filter_by(email=email).first()
        if not user:
            return 'User Not Found!', 404

        if user:
            access_token = create_access_token(identity=email)
            return jsonify(message='Login Successful', access_token=access_token)
        else:
            return 'Invalid Login Info!', 400


@app.route('/', methods=['POST', 'GET'])
#@jwt_required()
def home():
    if request.method == "POST":
        url_received = request.form["nm"]   #check if url in db
        found_url = Urls.query.filter_by(long=url_received).first()
        
        if found_url:                       #return short url, if found
            return redirect(url_for("display_short_url",url=found_url.short))
        
        else:                               #create short url, if not found
            short_url = shorten_url()
            new_url = Urls(url_received, short_url)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url", url=short_url))

    else:
        return render_template("home.html")

@app.route('/display/<url>')
def display_short_url(url):
    return render_template('shorturl.html',short_url_display=url)

@app.route('/<short_url>')
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return f'<h1> Url does not exist <h1>' 

if __name__ == '__main__':
    app.run(port=5000, debug=True)
