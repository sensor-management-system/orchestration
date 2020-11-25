import os


class BaseConfig:
    """Base configuration"""

    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "top_secret"

    DEFAULT_POOL_TIMEOUT = 600
    SQLALCHEMY_POOL_TIMEOUT = os.environ.get("POOL_TIMEOUT", DEFAULT_POOL_TIMEOUT)


class DevelopmentConfig(BaseConfig):
    """Development configuration"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL")


class TestingConfig(BaseConfig):
    """Testing configuration"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")
    ELASTICSEARCH_URL = None


class ProductionConfig(BaseConfig):
    """Production configuration"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL")
