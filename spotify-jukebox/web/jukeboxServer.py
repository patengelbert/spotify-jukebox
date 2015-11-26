# import the Flask class from the flask module
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, json
from flask.json import jsonify

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, \
    logout_user, login_required
    
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from sqlalchemy.exc import IntegrityError

from passlib.hash import pbkdf2_sha256

import requests
import re

# create the application object
app = Flask(__name__)
login_manager = LoginManager()
login_manager.setup_app(app)
app.config.from_pyfile('jukebox.cfg')

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
if not database_exists(engine.url):
    create_database(engine.url)
    
db = SQLAlchemy(app)


class UserNotFoundError(Exception):
    pass


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    password = db.Column(db.String(120))
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.first_name = None
        self.last_name = None
        self.password = password
        
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
        
    def __repr__(self):
        return '<User %r>' % self.username

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer)
    priority = db.Column(db.Integer)
    user_added = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, song_id, user_id):
        self.song_id = song_id
        self.priority = 0
        self.user_added = user_id
        
    def __repr__(self):
        return '<Song %r>' % self.song_id
    
db.create_all()


@login_manager.unauthorized_handler
def unauthorized():
    return render_template('main.html', error='Unauthorized')

# Flask-Login use this to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# use decorators to link the function to a url
@app.route('/')
@app.route('/home')
def home():
    return render_template('main.html')

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        id = request.form['username']
        password = pbkdf2_sha256.encrypt(request.form['password'], rounds=200000, salt_size=16)
        if pbkdf2_sha256.verify(request.form['passwordrepeat'], password):
            user = User(id, id, password)
            db.session.add(user)
            try:
                db.session.commit()
                login_user(user)
                return jsonify(), 200
            except IntegrityError:
                error = 'User already exists'
                return jsonify(error=error), 422
        else:
            error = 'Passwords are not identical'
            return jsonify(error=error), 301
    return render_template('register.html', error=error)

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    error = None
    if request.method == 'POST':
        user = current_user
        if request.form.get('firstname') != None and request.form.get('firstname') != user.first_name:
            user.first_name = request.form.get('firstname')
        if request.form.get('lastname') != None and request.form.get('lastname') != user.last_name:
            user.last_name = request.form.get('lastname')
        if request.form.get('password') != None and request.form.get('password') != user.password:
            user.password = pbkdf2_sha256.encrypt(request.form.get('password'), rounds=200000, salt_size=16)
        db.session.commit()
    return render_template('account.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # retrieve username and password
        user = User.query.filter_by(username=request.form['username']).first()
        if (user and pbkdf2_sha256.verify(request.form['password'], user.password)):
            remember_me = request.form.get('remember') is not None
            login_user(user, remember=remember_me)
            return jsonify(), 200
        else:
            error = 'Invalid Credentials. Please try again.'
            return jsonify(error=error), 301
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/toptracks')
def toptracks():
    page = requests.get('https://open.spotify.com/user/spotify/playlist/4hOKQuZbraPDIfaGbM3lKI').text
    values = re.findall('https://open.spotify.com/track/([a-zA-Z0-9]+)', page)
    return jsonify(values=values[:10]), 200

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run()


