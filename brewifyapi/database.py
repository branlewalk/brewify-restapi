import pymysql
import sys

class Database:
    
    def __init__(self):
        self.conn = None
        
    def init_app(self, app):
        self.host = app.config['DB_HOST']
        self.user = app.config['DB_USER']
        self.password = app.config['DB_PASSWORD']
        self.database = app.config['DB_DATABASE']
        self.port = app.config['DB_PORT']
        self.timeout = 5
        self.logger = app.logger
        
    def open_connection(self):
        try:
            if self.conn is None:
                self.conn = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    passwd=self.password,
                    db=self.database,
                    port=self.port,
                    connect_timeout=self.timeout 
                    )
        except pymysql.MySQLError as e:
            self.logger.error(e)
            #sys.exit()
            raise e
        finally:
            self.logger.debug('Connection opened successfully.')
            
    def close_connection(self):
        if self.conn:
                self.conn.close()
                self.conn = None
                self.logger.debug('Database connection closed.')
    
    def call_sproc_fetchone(self, sproc, params=None):
        try:
            self.open_connection()
            with self.conn.cursor() as cursor:
                if params != None:
                    cursor.callproc(sproc, params)
                else:
                    cursor.callproc(sproc)
                cursor.execute(f'SELECT @_{sproc}_{len(params)-1}')
                result = cursor.fetchone()
                self.conn.commit()
                cursor.close()
                return result[0]
        except pymysql.MySQLError as e:
            self.logger.error(e)
            raise e
        finally:
            self.close_connection()
            
    def call_sproc_fetchall(self, sproc, params=None):
        try:
            self.open_connection()
            with self.conn.cursor() as cursor:
                if params != None:
                    cursor.callproc(sproc, params)
                else:
                    cursor.callproc(sproc)
                result = cursor.fetchall()
                self.conn.commit()
                cursor.close()
                return result
        except pymysql.MySQLError as e:
            self.logger.error(e)
            raise e
            #sys.exit()
        finally:
            self.close_connection()