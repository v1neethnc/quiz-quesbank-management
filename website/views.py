from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from . import query_obj
from .helpers import DataInserter

views = Blueprint('views', __name__)

# Home page on successful login
@views.route('/home', methods=['GET', 'POST'])
def home():
	# Login updates the session variable
	if 'is_login' not in session:
		return render_template('404.html')
	return render_template("home.html")


# Temporary route that redirects to a specific set of pages
@views.route('redirect-page', methods=['GET'])
def redirect_page():
	# Data comes through a GET request from an anchor tag on home page
	page = request.args['page']
	
	# Redirect only if the user is logged in
	if 'is_login' in session:
		session['page'] = page
		
		# New record page
		if 'new' in page:
			return redirect(url_for('views.new_record'))
	
		# Display record page fetches the data and stores in the data_fetcher object
		# before redirecting to display records page
		if 'display' in page:
			query_obj.data_fetcher()
			return redirect(url_for('views.display_records'))
	
	return render_template('404.html')


# Route for pages to enter a new record into the database
@views.route("/new-record", methods=['GET', 'POST'])
def new_record():
	# Check if the user is logged in
	if 'is_login' not in session:
		return render_template('404.html')
		
	# After the form on the page is submitted
	if request.method == 'POST':
		data_dict = {}
		print(session['page'])

		# Check what kind of data is being entered into the database
		if 'idea' in session['page']:
			# Get the new idea record data and check if the idea field is not null
			data_dict['idea_index'] = request.form['idea_index']
			data_dict['author_id'] = session['author_id']
			data_dict['idea'] = request.form.get('idea')
			data_dict['sources'] = request.form.get('sources')
			if data_dict['sources'] is None:
				data_dict['sources'] = "N/A"
			if data_dict['idea'] is not None:
				insert_obj = DataInserter()
				# Successful or failure message flashing
				if insert_obj.insert_record('idea', data_dict):
					flash("Idea inserted into the database.", category="success")
				else:
					flash("Idea not inserted into the database.", category="error")
				# Regardless of success or failure, go to the home page
				return redirect(url_for('views.home'))
			# If the idea field is null, then flash an error message and stay on the new record page
			else:
				flash("Fill the Idea or Fact form to insert data into the database.", category="error")
				return render_template('new_record.html')
				
		# Entering new note into the database
		elif 'note' in session['page']:
			# Get the note text and check if it is null
			data_dict['note'] = request.form.get('note')
			if len(data_dict['note']) != 0:
				# If not null, then run the insert command
				insert_obj = DataInserter()
				# Flash a message based on the result of the insertion
				# If not null, then run the insert command
				if insert_obj.insert_record('note', data_dict):
					flash("Note inserted into the database.", category="success")
				else:
					flash("Note not inserted into the database.", category="error")
				return redirect(url_for('views.home'))
			else:
				# If the note is empty then prompt an error message and stay on the same page
				flash("Fill the Note form to insert data into the database.", category="error")
				return render_template('new_record.html')
	
	if 'idea' in session['page']:
		print(session)
		insert_obj = DataInserter()
		data = insert_obj.inserter_id_fetcher('ideasidfetcher')
		data.append(session['author'])
	return render_template('new_record.html', data=data)


# Route to the display records page
@views.route("/display-records", methods=['GET', 'POST'])
def display_records():
	# Check if the user is logged in
	if 'is_login' not in session:
		return render_template('404.html')

	# Fetch data from the query object's attributes
	data_used = [list(i) for i in query_obj.data_used]

	# Create empty lists that are to be used only when the page is display questions
	categories, quizzes, authors = [], [], []
	if 'question' in session['page']:
		# Update the lists for the display questions page
		categories = query_obj.names_indices_fetcher('categories')
		quizzes = query_obj.names_indices_fetcher('quizzes')
		authors = query_obj.names_indices_fetcher('authors')
		quizzes.append("N/A")
		authors.append("All")
		
	# If any of the three buttons are clicked
	if request.method == 'POST':
		# Check what kind of page this is and get corresponding button value
		# TO-DO: Add code for edit and delete buttons 
		if 'question' in session['page']:
			ques_operation = request.form.get('question_operation')
			operation, index = ques_operation.split(' ')[0], int(ques_operation.split(' ')[1]) - 1
			print(operation, index, data_used[index])
			if operation == 'more':
				session['page'] = 'single_question'
				session['data'] = data_used[index]
				return redirect(url_for('operations.single_record_display'))
		elif 'idea' in session['page']:
			q_type = request.form.get('idea_operation')
			operation, index = q_type.split(' ')[0], int(q_type.split(' ')[1]) - 1
			print(operation, index, data_used[index])
			# If the operation is to open the record in a new page
			if operation == 'more':
				# Update the session variables
				session['page'] = 'single_idea'
				session['data'] = data_used[index]
				# Redirect to the single record display function
				return redirect(url_for('operations.single_record_display'))
	# Default display records template
	return render_template('display_records.html', data=data_used, categories=categories, quizzes=quizzes, authors=authors)


@views.route("/test", methods=['GET'])
def test_val():
	if 'is_login' in session:
		return render_template("test.html")
	return render_template('404.html')