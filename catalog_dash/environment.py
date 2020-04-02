"""Get environment variables"""

from os import environ
from logging import DEBUG, INFO


os_environ_get = environ.get


DEBUG_MODE = bool(os_environ_get('DEBUG_MODE', 'False'))

# default logging level in production server
LOGGING_LEVEL = INFO

# if the application is in development mode, then change the logging level and debug mode
if DEBUG_MODE:
    LOGGING_LEVEL = DEBUG

# MYSQL connection
MYSQL_DB_USER = os_environ_get('MYSQL_DB_USER', 'test')
MYSQL_DB_PASSWORD = os_environ_get('MYSQL_DB_PASSWORD', 'test')
MYSQL_DB_HOST = os_environ_get('MYSQL_DB_HOST', 'localhost')
MYSQL_DB_PORT = os_environ_get('MYSQL_DB_PORT', '3306')
MYSQL_DB_DATABASE = os_environ_get('MYSQL_DB_DATABASE', 'database')
