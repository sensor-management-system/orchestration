import json
import os

from jwt.algorithms import RSAAlgorithm
from project.api.token_checker import oidc_jwks_uri


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
    # Setup Token Verification
    # force use of RS265
    JWT_ALGORITHM = "RS256"
    # retrieve first jwk entry from jwks_uri endpoint and use it to construct the RSA public key
    JWT_PUBLIC_KEY = RSAAlgorithm.from_jwk(json.dumps(oidc_jwks_uri["keys"][0]))
    # audience is oidc client id (can be array starting
    # https://github.com/vimalloc/flask-jwt-extended/issues/219)
    JWT_DECODE_AUDIENCE = ["rdmsvm-implicit-flow", "oidcdebugger-implicit-flow"]
    # name of token entry that will become distinct flask identity username
    JWT_IDENTITY_CLAIM = os.environ.get("OIDC_USERNAME_CLAIM")


class TestingConfig(BaseConfig):
    """Testing configuration"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")
    ELASTICSEARCH_URL = None


class ProductionConfig(BaseConfig):
    """Production configuration"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL")
