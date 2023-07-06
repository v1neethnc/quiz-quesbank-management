from . import mysql_obj
from datetime import datetime
from configparser import ConfigParser

class DataInserter():	
	def __init__(self):
		self.query_obj = mysql_obj
		self.data_used = None
		self.config = ConfigParser()
		self.config.read('website/inserters.cfg')

	def inserter_id_fetcher(self, data_type):
		return [i[0] for i in self.cursor_execution(self.config['inserters'][data_type])]

	def cursor_execution(self, query):
		"""
		Creates a cursor from the SQL object, executes the query, and returns the entire dataset fetched
		"""
		cursor = self.query_obj.connection.cursor()
		cursor.execute(query)
		return cursor.fetchall()

	def command_executer(self, command, data):
		print(command, data)
		cursor = self.query_obj.connection.cursor()
		cursor.execute(command, data)
		self.query_obj.connection.commit()
		return True

	def insert_record(self, record_type, data_dict):
		try:
			if record_type == 'idea':
				print(self.config.items('inserters'))
				insert_command = self.config['inserters']['ideainserter']
				print(data_dict)
				self.command_executer(insert_command, (data_dict['idea_index'], data_dict['idea'], data_dict['sources'], data_dict['author_id'], datetime.now(), datetime.now()))
			elif record_type == 'note':
				insert_command = 'insert into notes (notes_text, record_create_date, record_update_date) values (%s, %s, %s)'
				self.command_executer(insert_command, (data_dict['note'], datetime.now(), datetime.now()), "insert")
			return True
		except Exception as e:
			print(e)