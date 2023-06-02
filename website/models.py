from flask_login import UserMixin
from . import mysql_obj

class User(UserMixin):
    
	def __init__(self, username, password) -> None:
		super().__init__()
		self.username = username
		self.password = password

	def get(self):
		cursor = mysql_obj.connection.cursor()
		command = 'select * from user_credentials where username = %s and password = MD5(%s)'
		cursor.execute(command, (self.username, self.password))

		if cursor.rowcount == 1:
			return User(self.username, self.password)
		return None
		