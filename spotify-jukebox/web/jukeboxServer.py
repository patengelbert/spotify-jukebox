# import the Flask class from the flask module
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, json
from flask.json import jsonify
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from falsk.ext.sqlalchemy import SQLAlchemy

# create the application object
app = Flask(__name__)
login_manager = LoginManager()
login_manager.setup_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/[YOUR_DATABASE_NAME]'
db = SQLAlchemy(app)


class UserNotFoundError(Exception):
    pass

class UserDB(object):
    # proxy for a database of users
    user_database = {'admin@admin': {'pw': 'admin',
				    'first_name': 'Admin',
				    'last_name': 'admin'}}
    
    def add(self, user, pw):
        self.user_database[user] = {'pw': pw}

    def get(self, user):
        return (user, self.user_database.get(user))

    def update(self, user):
        self.user_database[user] = {'pw': user.password,
                                    'first_name':user.first_name,
                                    'last_name':user.last_name}

    
user_database = UserDB()

class User(UserMixin):

    def __init__(self, id):
        self.id, self.password = user_database.get(id)
	self.first_name = self.password.get('first_name')
	self.last_name = self.password.get('last_name')
	self.password = self.password['pw']
        if self.id is None or self.password is None:
            raise UserNotFoundError()

    @classmethod
    def get(self_class, id):
        '''Return user instance of id, return None if not exist'''
        try:
            return self_class(id)
        except UserNotFoundError:
            return None

    def update(self):
        user_database.update(self)

@login_manager.unauthorized_handler
def unauthorized():
    return render_template('main.html', error='Unauthorized')

# Flask-Login use this to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return User.get(id)

# use decorators to link the function to a url
@app.route('/')
@app.route('/home')
def home(errors=None):
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
        pass1 = request.form['password']
        pass2 = request.form['passwordrepeat']
        if (pass1 == pass2):
            user_database.add(id, pass1)
            user = User.get(id)
            login_user(user)
            return jsonify(), 200
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
        user.first_name = request.form.get('firstname')
        user.last_name = request.form.get('lastname')
        user.password = request.form.get('password')
        user.update()
    return render_template('account.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # retrieve username and password
        user = User.get(request.form['username'])
        if (user and user.password == request.form['password']):
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

app.secret_key = '"\x0fNG%\'w\xa30\xc1\83\xe7\xb9Ay\xbe\x0e\x13W\xc3\xd1d]\xba'

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)


