# import the Flask class from the flask module
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, json
from flask.json import jsonify
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user

# create the application object
app = Flask(__name__)
login_manager = LoginManager()
login_manager.setup_app(app)


class UserNotFoundError(Exception):
    pass

class User(UserMixin):
    # proxy for a database of users
    user_database = {'admin@admin': 'admin'}

    def __init__(self, id):
        if not id in self.user_database:
            raise UserNotFoundError()
        self.id = id
        self.password = self.user_database[id]


    @classmethod
    def get(self_class, id):
        '''Return user instance of id, return None if not exist'''
        try:
            return self_class(id)
        except UserNotFoundError:
            return None

# Flask-Login use this to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return User.get(id)

# use decorators to link the function to a url
@app.route('/')
@app.route('/home')
def home():
    return render_template('main.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # validate username and password
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

app.secret_key = '"\x0fNG%\'w\xa30\xc1\83\xe7\xb9Ay\xbe\x0e\x13W\xc3\xd1d]\xba'

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)


