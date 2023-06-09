from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from . import query_obj
from . import helpers

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

@views.route("/new-record", methods=['GET', 'POST'])
def new_record():
	if 'is_login' not in session:
		return render_template('404.html')
	if request.method == 'POST':
		data_dict = {}
		print(session['page'])
		if 'idea' in session['page']:
			data_dict['idea'] = request.form.get('idea')
			data_dict['sources'] = request.form.get('sources')
			if len(data_dict['idea']) != 0:
				insert_obj = helpers.data_inserter()
				if insert_obj.insert_record('idea', data_dict):
					flash("Idea inserted into the database.", category="success")
				else:
					flash("Idea not inserted into the database.", category="error")
				return redirect(url_for('views.home'))
			else:
				flash("Fill the Idea or Fact form to insert data into the database.", category="error")
				return render_template('new_record.html')
		elif 'note' in session['page']:
			data_dict['note'] = request.form.get('note')
			if len(data_dict['note']) != 0:
				insert_obj = helpers.data_inserter()
				if insert_obj.insert_record('note', data_dict):
					flash("Note inserted into the database.", category="success")
				else:
					flash("Note not inserted into the database.", category="error")
				return redirect(url_for('views.home'))
			else:
				flash("Fill the Note form to insert data into the database.", category="error")
				return render_template('new_record.html')
			
	return render_template('new_record.html')

@views.route("/display-records", methods=['GET', 'POST'])
def display_records():
	if 'is_login' not in session:
		return render_template('404.html')

	data_used = [list(i) for i in query_obj.data_used]
	categories, quizzes, authors = [], [], []
	if 'question' in session['page']:
		categories = query_obj.category_fetcher()
		quizzes = query_obj.quizzes_fetcher()
		authors = query_obj.authors_fetcher()
		quizzes.append("N/A")
	if request.method == 'POST':
		if 'question' in session['page']:
			q_id = request.form.get('id_val')
			print(q_id)
		if 'idea' in session['page']:
			q_type = request.form.get('idea_operation')
			print(q_type)

	return render_template('display_records.html', data=data_used, categories=categories, quizzes=quizzes, authors=authors)

@views.route("/test")
def test_val():
	if 'is_login' in session:
		return render_template("test.html")
	return render_template('404.html')