"""Get environment variables"""

from os import environ
from logging import DEBUG, INFO

from modules.utils import str2bool


os_environ_get = environ.get


# True: the application will get the data from the database
# False: the application will get the data from a CSV file
IS_TO_USE_DATA_FROM_DB = str2bool(os_environ_get('IS_TO_USE_DATA_FROM_DB', 'False'))

DEBUG_MODE = str2bool(os_environ_get('DEBUG_MODE', 'True'))

SERVER_HOST = os_environ_get('SERVER_HOST', '0.0.0.0')
SERVER_PORT = int(os_environ_get('SERVER_PORT', 8050))

# default logging level in production server
LOGGING_LEVEL = INFO

# if the application is in development mode, then change the logging level and debug mode
if DEBUG_MODE:
    LOGGING_LEVEL = DEBUG

# MYSQL connection
MYSQL_DB_USER = os_environ_get('MYSQL_DB_USER', 'test')
MYSQL_DB_PASSWORD = os_environ_get('MYSQL_DB_PASSWORD', 'test')
MYSQL_DB_HOST = os_environ_get('MYSQL_DB_HOST', 'localhost')
MYSQL_DB_PORT = int(os_environ_get('MYSQL_DB_PORT', 3306))
MYSQL_DB_DATABASE = os_environ_get('MYSQL_DB_DATABASE', 'database')
