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

class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SECRET_KEY="mysupersecretkey"
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = DATABASE_URL="postgresql://postgres:deepdot123@localhost/test_db"
    DEBUG = True

class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    Testing = False

app_config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}