import os

class BaseConfig:
    SECRET_KEY = 'A SECRET KEY'
    FLASK_SECRET = SECRET_KEY

class DevConfig(BaseConfig):
    DEBUG = True
    DEVELOPMENT = True
    DB_HOST = 'localhost'
    DB_PORT = 3306
    DB_DATABASE = 'brewify_db'
    DB_USER = 'root'
    DB_PASSWORD = 'password'
    

class TestConfig(BaseConfig):
    DEBUG = True
    DEVELOPMENT = True
    DB_HOST = 'localhost'
    DB_PORT = 3306
    DB_DATABASE = 'brewify_db'
    DB_USER = 'root'
    DB_PASSWORD = 'password' 

class ProdConfig(BaseConfig):
    DEBUG = False
    DEVELOPMENT = False
    DB_HOST = 'localhost'
    DB_PORT = 3306
    DB_DATABASE = 'brewify_db'
    DB_USER = 'root'
    DB_PASSWORD = 'password' 