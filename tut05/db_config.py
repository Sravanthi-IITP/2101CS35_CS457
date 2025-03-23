from flask_mysqldb import MySQL

def init_db(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''  # No password for XAMPP MySQL
    app.config['MYSQL_DB'] = 'role_based_access'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


    return MySQL(app)
