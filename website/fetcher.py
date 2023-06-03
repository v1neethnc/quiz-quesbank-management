from flask import session
from datetime import datetime

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
			clause = ''
			if val == 'quiz':
				clause = ' order by date_of_quiz asc'
			return f"select * from {table_map[val]}{clause}"
		return f"select * from questions_data"

	def data_fetcher(self):
		command = self.select_query()
		cursor = self.query_obj.connection.cursor()
		cursor.execute(command)
		data = cursor.fetchall()
		self.data_used = self.data_preprocessor(data)

	def data_preprocessor(self, data):
		if 'idea' in session['page']:
			temp = []
			for line in data:
				idea = line[1][:47] + "..." if len(line[1]) > 50 else line[1]
				tmp = [line[0], idea, line[2], line[3], line[1]]
				temp.append(tmp)
			return temp
		if 'question' in session['page']:
			temp = []
			for line in data:
				question = line[1][:47] + "..." if len(line[1]) > 50 else line[1]
				answer = line[2][:22] + "..." if len(line[2]) > 25 else line[2]
				explanation = line[3][:22] + "..." if len(line[3]) > 25 else line[3]
				date_val = line[5].strftime("%d-%m-%Y")
				author = 'Ashwin' if line[6] == 'A' else "Vineeth"
				media = line[7][:22] + "..." if len(line[7]) > 25 and line[7] is not None else line[7]
				ques = line[1].replace("\\n", '\n')
				ans = line[2].replace("\\n", '\n')
				expl = line[3].replace("\\n", '\n')
				tmp = [line[0], question, answer, explanation, line[4], date_val, author, media, line[9], ques, ans, expl]
				temp.append(tmp)
			return(temp)
		if 'quiz' in session['page']:
			temp = []
			print(data[0])
			for line in data:
				title = line[2][:30] + "..." if len(line[2]) > 30 else line[2]
				date_val = line[5].strftime("%d-%m-%Y")
				reception = line[13][:22] + "..." if len(line[13]) > 25 else line[13]
				tmp = [line[0], line[1], title, line[3], line[4], date_val, line[6], line[12], reception]
				temp.append(tmp)
			return temp