# import the Flask class from the flask module
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, json
from flask.json import jsonify

# create the application object
app = Flask(__name__)

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
        user = request.form['username']
        pw = request.form['password']
        if user != 'admin@admin' or pw != 'admin':
            error = 'Invalid Credentials. Please try again.'
            return jsonify(error=error), 301
        else:
            session['logged_in'] = True
            return jsonify(), 200
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

app.secret_key = '"\x0fNG%\'w\xa30\xc1\83\xe7\xb9Ay\xbe\x0e\x13W\xc3\xd1d]\xba'

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)


