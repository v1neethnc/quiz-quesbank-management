from . import app
from flask_mysqldb import MySQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'vineeth'
app.config['MYSQL_PASSWORD'] = 'd0r1t0sch33t0sfr1t0s'
app.config['MYSQL_DB'] = 'quiz_db'
mysql_obj = MySQL()
mysql_obj.init_app(app)


from .auth import auth
app.register_blueprint(auth, url_prefix='/')