"""Get environment variables"""

from os import environ
from logging import DEBUG, INFO


os_environ_get = environ.get


FLASK_ENV = os_environ_get('FLASK_ENV', 'production')

# default logging level in production server
LOGGING_LEVEL = INFO
# default debug mode in production server
DEBUG_MODE = False

# if the application is in development mode, then change the logging level and debug mode
if FLASK_ENV == 'development':
    LOGGING_LEVEL = DEBUG
    DEBUG_MODE = True

# MYSQL connection
MYSQL_DB_USER = os_environ_get('MYSQL_DB_USER', 'test')
MYSQL_DB_PASSWORD = os_environ_get('MYSQL_DB_PASSWORD', 'test')
MYSQL_DB_HOST = os_environ_get('MYSQL_DB_HOST', 'localhost')
MYSQL_DB_PORT = os_environ_get('MYSQL_DB_PORT', '3306')
MYSQL_DB_DATABASE = os_environ_get('MYSQL_DB_DATABASE', 'database')
