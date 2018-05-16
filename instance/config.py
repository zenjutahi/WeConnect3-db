import os
basedir = os.path.abspath(os.path.dirname(__file__))




class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments
    DEBUG = False
    CSRF_ENABLED = True
    JWT_BLACKLIST_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('EMAIL')
    MAIL_PASSWORD = os.environ.get('PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('EMAIL')

class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI ="postgresql://postgres:deepdot123@localhost/test_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    DEBUG = True

class ProductionConfig(Config):
    """
    Production configurations
    """

    TESTING = False

app_config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
