from dotenv import load_dotenv
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# .env 파일 auto load
load_dotenv()

class Config:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY') or 'hard to guess string'

    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_RECORD_QUERIES = True

class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    
    # SQLALCHEMY_DATABASE_URI = f"mysql://{os.getenv('DB_USER')}:" \
    #                           f"{os.getenv('DB_PWD')}@" \
    #                           f"{os.getenv('DB_HOST')}:" \
    #                           f"{os.getenv('DB_PORT')}/" \
    #                           f"{os.getenv('DB_NAME')}?charset=utf8"

    MYSQL_USER = os.getenv('DEV_DB_USER') or 'root'
    MYSQL_PASSWORD = os.getenv('DEV_DB_PWD') or ''
    MYSQL_HOST = os.getenv('DEV_DB_HOST') or 'localhost'
    MYSQL_PORT = int(os.getenv('DEV_DB_PORT')) or 3306
    MYSQL_DB = os.getenv('DEV_DB_NAME') or 'testdb'

    WTF_CSRF_ENABLED = False
    
class ProductionConfig(Config):
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    MYSQL_USER = os.getenv('PROD_DB_USER')
    MYSQL_PASSWORD = os.getenv('PROD_DB_PWD')
    MYSQL_HOST = os.getenv('PROD_DB_HOST')
    MYSQL_PORT = int(os.getenv('DEV_DB_PORT'))
    MYSQL_DB = os.getenv('PROD_DB_NAME')
    
    WTF_CSRF_ENABLED = False


# reference : https://github.com/miguelgrinberg/flasky/blob/master/config.py