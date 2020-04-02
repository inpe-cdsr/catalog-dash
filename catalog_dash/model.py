# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

from werkzeug.exceptions import InternalServerError

from catalog_dash.environment import MYSQL_DB_USER, MYSQL_DB_PASSWORD, MYSQL_DB_HOST, \
                                     MYSQL_DB_PORT, MYSQL_DB_DATABASE
from catalog_dash.log import logging

# logging.info('model.py - MYSQL_DB_USER: %s', MYSQL_DB_USER)
# logging.info('model.py - MYSQL_DB_PASSWORD: %s', MYSQL_DB_PASSWORD)
# logging.info('model.py - MYSQL_DB_HOST: %s', MYSQL_DB_HOST)
# logging.info('model.py - MYSQL_DB_PORT: %s', MYSQL_DB_PORT)
# logging.info('model.py - MYSQL_DB_DATABASE: %s\n', MYSQL_DB_DATABASE)

# def fix_rows(rows):
#     for row in rows:
#         for key in row:
#             # datetime/date is not serializable by default, then it gets a serializable string representation
#             if isinstance(row[key], (datetime, date)):
#                 row[key] = row[key].isoformat()

#     return rows

class DatabaseConnection():
    # Source: https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html

    def __init__(self):
        self.engine = None

    def connect(self):
        try:
            self.engine = create_engine('mysql://{}:{}@{}:{}/{}'.format(
                MYSQL_DB_USER, MYSQL_DB_PASSWORD, MYSQL_DB_HOST,
                MYSQL_DB_PORT, MYSQL_DB_DATABASE
            ))

        except SQLAlchemyError as error:
            error_message = 'An error occurred during database connection'

            logging.error('DatabaseConnection.connect() - error.code: %s', error.code)
            logging.error('DatabaseConnection.connect() - error.args: %s', error.args)
            logging.error('DatabaseConnection.connect() - %s: %s\n', error_message, error)

            # error_message += ': ' + str(error.args)

            self.close()
            raise InternalServerError(error_message)

    def close(self):
        if self.engine is not None:
            self.engine.dispose()

        self.engine = None

    def try_to_connect(self):
        attempt = 0

        # while engine is None, try to connect
        while self.engine is None and attempt < 3:
            attempt += 1
            self.connect()

        if attempt >= 3:
            self.close()
            raise DatabaseConnectionException('Connection was not opened to the database.')

    def execute(self, query, params=None, is_transaction=False):
        logging.info('DatabaseConnection.execute()')

        # sometimes there are a lot of blank spaces, then I remove it
        query = query.replace('            ', '')

        # logging.info('DatabaseConnection.execute() - query: %s', query)
        # logging.debug('DatabaseConnection.execute() - params: %s', params)
        logging.info('DatabaseConnection.execute() - is_transaction: %s', is_transaction)

        try:
            # if query is a transaction statement, then commit the changes
            if is_transaction:
                query_text = text(query).execution_options(autocommit=True)
            else:
                query_text = text(query)

            logging.info('DatabaseConnection.execute() - query_text: %s', query_text)

            self.try_to_connect()

            # cursor.execute(query, params=params)
            result = self.engine.execute(query_text, params)

            logging.info('DatabaseConnection.execute() - result.returns_rows: %s', result.returns_rows)
            logging.info('DatabaseConnection.execute() - result.rowcount: %s', result.rowcount)
            logging.info('DatabaseConnection.execute() - result.lastrowid: %s', result.lastrowid)

            if result.returns_rows:
                # SELECT clause
                rows = result.fetchall()
                rows = [dict(row) for row in rows]

                # logging.info('DatabaseConnection.execute() - rows: \n%s\n', rows)

                return rows
            else:
                # INSERT, UPDATE and DELETE operations need to be committed
                # if 'query' was a 'INSERT' statement, then it returns the inserted record 'id',
                # else it returns '0'
                return str(result.lastrowid)

        except SQLAlchemyError as error:
            # self.rollback()
            error_message = 'An error occurred during query execution'

            logging.error('DatabaseConnection.execute() - error.code: %s', error.code)
            logging.error('DatabaseConnection.execute() - error.args: %s', error.args)
            logging.error('DatabaseConnection.execute() - %s: %s\n', error_message, error)

            error_message += ': ' + str(error.args)

            raise InternalServerError(error_message)

        # finally is always executed (both at try and except)
        finally:
            self.close()
            # print('Database connection was closed.')

    def select_from_graph_amount_scenes_by_dataset_and_date(self):
        query = '''
            SELECT * FROM `graph_amount_scenes_by_dataset_and_date`;
        '''

        # return fix_rows(self.execute(query, params))
        return self.execute(query, {})
