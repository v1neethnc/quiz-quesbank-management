from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from . import mysql_obj

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		cursor = mysql_obj.connection.cursor()
		
		command = 'select * from user_credentials where username = %s and password = MD5(%s)'
		cursor.execute(command, (username, password))

		if cursor.rowcount == 1:
			flash("Logged in, I suppose", category='success')
			command = 'select author_name, author_id from authors where username= %s'
			cursor.execute(command, [username])
			author_details = cursor.fetchall()
			session['is_login'] = True
			session['username'] = username
			session['page'] = 'home'
			session['author'] = author_details[0][0]
			session['author_id'] = author_details[0][1]
			return redirect(url_for('views.home'))
		else:
			flash("Incorrect credentials", category='error')
	if 'is_login' in session:
		return render_template('home.html')
	return render_template("login.html")

@auth.route('logout')
def logout():
	keys = [i for i in session.keys()]
	for k in keys:
		session.pop(k, None)
	# session.pop('is_login', None)
	# session.pop('username', None)
	# session.pop('page', None)
	return redirect(url_for('auth.login'))