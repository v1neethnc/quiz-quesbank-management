from flask_login import UserMixin
from . import mysql_obj

class User(UserMixin):
	def __init__(self, username, password) -> None:
		"""
		The username and the MD5 hash of the password are needed.
		"""
		super().__init__()
		self.username = username
		self.password = password

	def get(self):
		"""
		Checks if the user with the corresponding password hash exists.
		"""
		cursor = mysql_obj.connection.cursor()
		command = 'select * from user_credentials where username = %s and password = MD5(%s)'
		cursor.execute(command, (self.username, self.password))

		# If there is only one row returned, it means a unique user exists.
		if cursor.rowcount == 1:
			return User(self.username, self.password)
		return None
		