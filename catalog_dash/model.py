# -*- coding: utf-8 -*-

from pandas import read_sql
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError

from catalog_dash.environment import MYSQL_DB_USER, MYSQL_DB_PASSWORD, MYSQL_DB_HOST, \
                                     MYSQL_DB_PORT, MYSQL_DB_DATABASE
from catalog_dash.log import logging


class DatabaseConnection():

    def __init__(self):
        self.engine = None

    def connect(self):
        try:
            self.engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(
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

    def execute(self, query):
        logging.info('DatabaseConnection.execute()\n')

        try:
            logging.info('DatabaseConnection.execute() - query: %s\n', query)

            self.try_to_connect()

            df = read_sql(query, con=self.engine)

            logging.info('DatabaseConnection.execute() - df.head(): \n%s\n', df.head())
            logging.info('DatabaseConnection.execute() - df.shape: %s\n', df.shape)
            logging.info('DatabaseConnection.execute() - df.dtypes: \n%s\n', df.dtypes)

            return df

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

    def select_from_graph_amount_scenes_by_dataset_and_date(self):
        return self.execute('SELECT * FROM `graph_amount_scenes_by_dataset_and_date`;')
