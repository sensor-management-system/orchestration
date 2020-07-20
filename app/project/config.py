import os


class BaseConfig:  # pylint: disable=too-few-public-methods
    """Base configuration"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'top_secret'

    DEFAULT_POOL_TIMEOUT = 600
    SQLALCHEMY_POOL_TIMEOUT = os.environ.get('POOL_TIMEOUT', DEFAULT_POOL_TIMEOUT)


class DevelopmentConfig(BaseConfig):  # pylint: disable=too-few-public-methods
    """Development configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(BaseConfig):  # pylint: disable=too-few-public-methods
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')


class ProductionConfig(BaseConfig):  # pylint: disable=too-few-public-methods
    """Production configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
