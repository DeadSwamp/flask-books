DEBUG = True
#dialect+driver://root:1q2w3e4r5t@127.0.0.1:3306/
DIALECT = 'mysql'
DRIVER='pymysql'
USERNAME = 'root'
PASSWORD = 'flask2021!'
HOST = 'localhost'
PORT = 3306
DATABASE = 'flask_sql_demo'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
print(SQLALCHEMY_DATABASE_URI)
