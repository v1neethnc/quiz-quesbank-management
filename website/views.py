from flask import Blueprint, render_template, session, request, redirect, url_for

views = Blueprint('views', __name__)

# Decorator
@views.route('/home', methods=['GET', 'POST'])
def home():
	if 'is_login' in session:
		return render_template("home.html")
	return render_template('404.html')

@views.route('/redirect-page', methods=['GET'])
def redirect_page():
	page = request.args['page']
	if 'is_login' in session:
		session['page'] = page
		if 'new' in page:
			return redirect(url_for('views.new_record'))
	return render_template('404.html')
		# if 'update' in page:
		# 	ret


@views.route("/new-record")
def new_record():
	return render_template('new_record.html')