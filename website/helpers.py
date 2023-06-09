from . import mysql_obj
from datetime import date

class data_inserter():
	
	def insert_record(self, record_type, data_dict):
		try:
			cursor = mysql_obj.connection.cursor()
			if record_type == 'idea':
				command = 'select max(idea_index) from question_ideas'
				cursor.execute(command)
				data = cursor.fetchall()
				print(type(data[0][0]))
				new_index = data[0][0] + 1
				insert_command = 'insert into question_ideas (idea_index, idea_fact, sources, is_framed) values (%s, %s, %s, "FALSE")'
				cursor.execute(insert_command, (new_index, data_dict['idea'], data_dict['sources']))
				mysql_obj.connection.commit()
			elif record_type == 'note':
				insert_command = 'insert into notes (notes_text, record_create_date, record_update_date) values (%s, %s, %s)'
				cursor.execute(insert_command, (data_dict['note'], date.today(), date.today()))
				mysql_obj.connection.commit()
			return True
		except:
			return False