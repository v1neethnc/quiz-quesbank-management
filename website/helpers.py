from . import mysql_obj
from datetime import date

class DataInserter():	
	def __init__(self):
		self.query_obj = mysql_obj

	def command_executer(self, command, data, tp = "select"):
		cursor = self.sql_obj.connection.cursor()
		cursor.execute(command, data)
		if tp == "select":
			return cursor.fetchall()
		self.sql_obj.connection.commit()
		return True

	def insert_record(self, record_type, data_dict):
		try:
			if record_type == 'idea':
				command = 'select max(idea_index) from question_ideas'
				data = self.command_executer(command, (), "select")
				print(type(data[0][0]))
				new_index = data[0][0] + 1
				insert_command = 'insert into question_ideas (idea_index, idea_fact, sources, is_framed) values (%s, %s, %s, "FALSE")'
				self.command_executer(insert_command, (new_index, data_dict['idea'], data_dict['sources']), "insert")
			elif record_type == 'note':
				insert_command = 'insert into notes (notes_text, record_create_date, record_update_date) values (%s, %s, %s)'
				self.command_executer(insert_command, (data_dict['note'], date.today(), date.today()), "insert")
			return True
		except:
			return False