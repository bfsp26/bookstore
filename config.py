class Config:
    SECRET_KEY = ':LQA1O9u9u%;lPC^b{tB'


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'netlab123'
    MYSQL_DB = 'bookstore'


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}