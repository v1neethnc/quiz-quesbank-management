from flask import session
from configparser import ConfigParser

class data_fetcher:
    
	def __init__(self, sql_obj):
		self.query_obj = sql_obj
		self.is_active = False
		self.data_used = None
		self.config = ConfigParser()
		self.config.read('config.cfg')

	def activate_obj(self):
		if not self.is_active:
			self.is_active = True

	def select_query(self):
		table_map = {'idea': 'question_ideas', 'quiz': 'quizzes', 'note': 'notes'}
		val = session['page'].split('_')[1]

		if val in table_map.keys():
			clause = ''
			if val == 'quiz':
				clause = ' order by date_of_quiz asc'
			elif val == 'note':
				clause = ' order by record_update_date asc'
			return f"select * from {table_map[val]}{clause}"
		return f"select * from questions_data"

	def data_fetcher(self):
		command = self.select_query()
		data = self.cursor_execution(command)
		self.data_used = self.data_preprocessor(data)

	def length_reducer(self, str_list, len_list):
		res_strs = []
		for string, length in zip(str_list, len_list):
			res_strs.append(string[:length-3] + "..." if len(string) > length else string)
		return res_strs
	
	def cursor_execution(self, query):
		cursor = self.query_obj.connection.cursor()
		cursor.execute(query)
		return cursor.fetchall()
	
	def category_fetcher(self):
		command = 'select category_name from categories'
		return [i[0] for i in self.cursor_execution(command)]
	
	def subcategory_fetcher(self):
		command = 'select subcategory_name from subcategories'
		return [i[0] for i in self.cursor_execution(command)]

	def quizzes_fetcher(self):
		command = 'select quiz_index from quizzes'
		return [i[0] for i in self.cursor_execution(command)]

	def authors_fetcher(self):
		command = 'select distinct owner from questions_data'
		return [self.config['names']['v1'] if auth[0] == self.config['names']['v1'][0] else self.config['names']['v2'] for auth in self.cursor_execution(command)]

	def data_preprocessor(self, data):
		temp = []
		if 'idea' in session['page']:
			for line in data:
				idea, sources = self.length_reducer([line[1], line[2]], [70, 30])
				tmp = [line[0], idea, sources, line[3], line[1], line[2]]
				temp.append(tmp)
			
		if 'question' in session['page']:
			for line in data:
				question, answer, explanation, media = self.length_reducer([line[1], line[2], line[3], line[7]], [50, 25, 25, 25])
				date_val = line[5].strftime("%d-%m-%Y")
				author = self.config['names']['v1'] if line[6] == 'A' else self.config['names']['v2']
				ques = line[1].replace("\\n", '\n')
				ans = line[2].replace("\\n", '\n')
				expl = line[3].replace("\\n", '\n')
				tmp = [line[0], question, answer, explanation, line[4], date_val, author, media, line[9], ques, ans, expl]
				temp.append(tmp)

		if 'quiz' in session['page']:
			for line in data:
				title, reception = self.length_reducer([line[2], line[13]], [30, 25])
				date_val = line[5].strftime("%d-%m-%Y")
				tmp = [line[0], line[1], title, line[3], line[4], date_val, line[6], line[12], reception, line[2], line[13]]
				temp.append(tmp)
		
		if 'note' in session['page']:
			for line in data:
				note = self.length_reducer([line[1]], [75])
				create_date = line[2].strftime("%d-%m-%Y")
				update_date = line[3].strftime("%d-%m-%Y")
				tmp = [note[0], create_date, update_date, line[1]]
				temp.append(tmp)
		return temp