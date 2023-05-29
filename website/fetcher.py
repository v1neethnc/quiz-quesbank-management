from flask import session

class data_fetcher:
    
	def __init__(self, sql_obj):
		self.query_obj = sql_obj
		self.is_active = False
		self.data_used = None

	def activate_obj(self):
		if not self.is_active:
			self.is_active = True

	def select_query(self):
		table_map = {'idea': 'question_ideas', 'quiz': 'quizzes', 'note': 'notes'}
		val = session['page'].split('_')[1]
		if val in table_map.keys():
			return f"select * from {table_map[val]}"
		return f"select * from questions_data"

	def data_fetcher(self):
		command = self.select_query()
		cursor = self.query_obj.connection.cursor()
		cursor.execute(command)
		# print(cursor.rowcount)
		data = cursor.fetchall()
		self.data_used = data
		# print(data)