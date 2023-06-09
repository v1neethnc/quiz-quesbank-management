from flask import session
from configparser import ConfigParser

class DataFetcher:
	def __init__(self, sql_obj):

		"""
		The attributes are as follows:
		query_obj: contains the MySQL object
		data_used: contains the data fetched from the last select query
		config: ConfigParser object that reads the relevant config file

		This class as of 17 June 2023 is primarily used for the display_records page.
		"""
		self.query_obj = sql_obj
		self.data_used = None
		self.config = ConfigParser()
		self.config.read('website/queries.cfg')

	def select_query(self):
		"""
		Method to identify the page and return the relevant select query for display pages
		"""
		# Get the page type and return the select query from the config file for display
		page = session['page'].split('_')[1]
		return self.config['display_queries'][page]

	def data_fetcher(self):

		"""
		Runs the select queries and writes data into the data_used attribute
		"""
		command = self.select_query()
		data = self.cursor_execution(command)
		self.data_used = self.data_preprocessor(data)

	def length_reducer(self, str_list, len_list):
		"""
		Given a list of strings and a list of maximum allowed lengths, the method returns a list of 
		values with the string terminated by an ellipsis, limiting the length to max allowed length
		"""
		res_strs = []
		for string, length in zip(str_list, len_list):
			res_strs.append(string[:length-3] + "..." if len(string) > length else string)
		return res_strs
	
	def cursor_execution(self, query):
		"""
		Creates a cursor from the SQL object, executes the query, and returns the entire dataset fetched
		"""
		"""
		Creates a cursor from the SQL object, executes the query, and returns the entire dataset fetched
		"""
		cursor = self.query_obj.connection.cursor()
		cursor.execute(query)
		return cursor.fetchall()
	
	# def category_fetcher(self):
	# 	"""
	# 	Fetches category names from the database, primarily for the filter on display_questions
	# 	"""
	# 	command = 'select category_name from categories'
	# 	return [i[0] for i in self.cursor_execution(command)]
	
	# def subcategory_fetcher(self):
	# 	"""
	# 	Fetches subcategory names from the database, primarily for the filter on display_questions
	# 	"""
	# 	command = 'select subcategory_name from subcategories'
	# 	return [i[0] for i in self.cursor_execution(command)]

	# def quizzes_fetcher(self):
	# 	"""
	# 	Fetches quizzes indices from the database, primarily for the filter on display_questions
	# 	"""
	# 	command = 'select quiz_index from quizzes'
	# 	return [i[0] for i in self.cursor_execution(command)]

	# def authors_fetcher(self):
	# 	"""
	# 	Fetches author names from the database, primarily for the filter on display_questions
	# 	"""
	# 	command = 'select distinct owner from questions_data'
	# 	return [self.config['names']['v1'] if auth[0] == self.config['names']['v1'][0] else self.config['names']['v2'] for auth in self.cursor_execution(command)]

	def names_indices_fetcher(self, page):
		"""
		Fetches the names and indices from specific tables for populating dropdown lists.
		names for categories, subcategories, and authors
		indices for quizzes
		"""
		return [i[0] for i in self.cursor_execution(self.config['names_indices'][page])]

	def data_preprocessor(self, data):
		"""
		To perform length reduction and convert datetime objects into proper dates to aid best display
		standards. The final results are stored in data_to_display. The data stored in data_used is processed
		for the display pages. For columns put through length_reducer, the full data is also sent in the variable
		line_to_display so that they may be displayed as a tooltip on the actual webpage.
		"""
		data_to_display = []
		
		# Display ideas
		# r_ => column after length_reducer
		# f_ => actual column data before length_reducer
		"""
		To perform length reduction and convert datetime objects into proper dates to aid best display
		standards. The final results are stored in data_to_display. The data stored in data_used is processed
		for the display pages. For columns put through length_reducer, the full data is also sent in the variable
		line_to_display so that they may be displayed as a tooltip on the actual webpage.
		"""
		data_to_display = []
		
		# Display ideas
		# r_ => column after length_reducer
		# f_ => actual column data before length_reducer
		if 'idea' in session['page']:
			# The order of data is: 
			# index, r_idea, r_sources, is_framed, f_idea, f_sources
			for line in data:
				idea, sources = self.length_reducer([line[1], line[2]], [60, 30])
				line_to_display = [line[0], idea, sources, line[3], line[4], line[1], line[2]]
				data_to_display.append(line_to_display)
		
		# Display questions
		if 'question' in session['page']:
			# The order of data is:
			# index, r_question, r_answer, r_explanation, idea index, created date, author, r_categories, used in, f_question, f_answer, f_explanation, f_categories
			# index, question_text, answer, explanation, idea_index, cnm, create_date, qd.owner, qd.used_in, qcl.snm
			for line in data:
				question, answer, explanation, categories, subcategories, quizzes = self.length_reducer([line[1], line[2], line[3], line[5].replace(',', ', '), line[6].replace(',', ', '),  line[10]], [45, 20, 25, 25, 25, 10])
				date_val = line[8].strftime('%d-%m-%Y')
				author = line[7]
				ques = line[1].replace('\\n', '\n')
				ans = line[2].replace('\\n', '\n')
				expl = line[3].replace('\\n', '\n')
				line_to_display = [line[0], question, answer, explanation, line[4], date_val, author, categories, quizzes, ques, ans, expl, line[10].replace(',', ', '), line[5].replace(',', ', '), subcategories, line[6].replace(',', ', ')]
				data_to_display.append(line_to_display)

		# Display quizzes
		# Display quizzes
		if 'quiz' in session['page']:
			# The order of data is:
			# quiz_id, event, r_title, quizmasters, venue, date of quiz, number of questions, reception, r_remarks, f_title, f_remarks
			for line in data:
				title, reception = self.length_reducer([line[2], line[13]], [30, 25])
				date_val = line[5].strftime('%d-%m-%Y')
				line_to_display = [line[0], line[1], title, line[3], line[4], date_val, line[6], line[12], reception, line[2], line[13]]
				data_to_display.append(line_to_display)
				date_val = line[5].strftime('%d-%m-%Y')
				line_to_display = [line[0], line[1], title, line[3], line[4], date_val, line[6], line[12], reception, line[2], line[13]]
				data_to_display.append(line_to_display)

		# Display notes
		if 'note' in session['page']:
			# The order of data is:
			# r_note, create date, last updated date, f_note
			for line in data:
				note = self.length_reducer([line[0]], [75])
				create_date = line[2].strftime('%d-%m-%Y')
				update_date = line[3].strftime('%d-%m-%Y')
				line_to_display = [note[0], line[1], create_date, update_date, line[0]]
				data_to_display.append(line_to_display)
		
		return data_to_display