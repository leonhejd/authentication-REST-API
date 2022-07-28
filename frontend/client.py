from flask import Flask, render_template, request, redirect, session
from functools import wraps
from modules import endpoint
import secrets 
app = Flask(__name__)

################################################################################
#
#					Authentication  API demo
#					  Author: Leon Philip
#
###############################################################################

app.config['SECRET_KEY'] = secrets.token_urlsafe()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_name') is None:
            return redirect('/', code=302)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
	error = None
	user_email = request.form.get('email')
	user_password = request.form.get('password')
	status, result = endpoint.login(user_email, user_password)
	if status == True:
		session['user_name'] = result['name']
		session['user_id'] = result['id']
		session['session_token'] = result['session_token']
		return redirect('/home')
	else: 
		error = result

	return render_template('index.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
	error = ''
	if request.method == 'POST':
		user_name = request.form.get('name')
		user_email = request.form.get('email')
		user_password = request.form.get('password')
		status, result = endpoint.register_user(user_name, user_email, user_password)
		if status == True:
			return redirect('/')
		else:
			error = result

	return render_template('register.html', error=error)

@app.route('/home', methods=['GET'])
@login_required
def home():
	return render_template('home.html')

@app.route('/logout', methods=['POST'])
def logout():
	if session.get('session_token'):
		status, result = endpoint.logout(session['session_token'])
		session.pop('user_name', None)
		session.pop('user_id', None)
		session.pop('session_token', None)
	return redirect('/')

@app.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
	return render_template('delete_account.html')

@app.route('/filter_users', methods=['GET', 'POST'])
@login_required
def filter_users():
	return render_template('filter_users.html')

@app.route('/request_password_reset', methods=['GET', 'POST'])
def request_password_reset():
	return render_template('request_password_reset.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
	return render_template('reset_password.html')

if __name__ == '__main__':
	app.run(port=8080, debug=False)
