from flask import Flask
from flask_mysqldb import MySQL
from configparser import ConfigParser
from website.fetcher import DataFetcher

mysql_obj = MySQL()
query_obj = DataFetcher(mysql_obj)

def create_app():
	
	app = Flask(__name__)
	
	# Read data from the config file
	config = ConfigParser()
	config.read('config.cfg')
	for i in ['SECRET_KEY', 'MYSQL_HOST', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DB']:
		app.config[i] = config['init_file'][i]
	mysql_obj.init_app(app)

	# Register different paths
	from .auth import auth
	from .views import views
	from .operations import operations
	app.register_blueprint(auth, url_prefix='/')
	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(operations, url_prefix='/')
	return app