from flask import Blueprint, render_template, session, request, redirect, url_for
from . import query_obj

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
		if 'display' in page:
			query_obj.data_fetcher()
			return redirect(url_for('views.display_records'))
	return render_template('404.html')

@views.route("/new-record")
def new_record():
	return render_template('new_record.html')

@views.route("/display-records", methods=['GET', 'POST'])
def display_records():
	data_used = [list(i) for i in query_obj.data_used]
	if request.method == 'POST':
		if 'question' in session['page']:
			q_id = request.form.get('id_val')
			print(q_id)
		if 'idea' in session['page']:
			q_type = request.form.get('idea_operation')
			print(q_type)
	return render_template('display_records.html', data=data_used)