from flask import Flask
from flask_mysqldb import MySQL
from configparser import ConfigParser
from website.fetcher import data_fetcher

mysql_obj = MySQL()
query_obj = data_fetcher(mysql_obj)

def create_app():
	
	app = Flask(__name__)
	
	config = ConfigParser()
	config.read('config.cfg')
	for i in ['SECRET_KEY', 'MYSQL_HOST', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DB']:
		app.config[i] = config['init_file'][i]
	mysql_obj.init_app(app)

	from .auth import auth
	from .views import views
	app.register_blueprint(auth, url_prefix='/')
	app.register_blueprint(views, url_prefix='/')
	
	return app