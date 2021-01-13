import json
import os

import requests
from jwt.algorithms import RSAAlgorithm


class Singleton(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
            oidc_issuer_url = os.environ.get("WELL_KNOWN_URL")
            # retrieve master openid-configuration endpoint for issuer realm
            oidc_config = requests.get(oidc_issuer_url, verify=False).json()
            # # retrieve data from jwks_uri endpoint
            oidc_jwks_uri = requests.get(oidc_config["jwks_uri"], verify=False).json()
            cls._instance = oidc_jwks_uri
        return cls._instance


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
    oidc_jwks_uri = Singleton()
    # retrieve first jwk entry from jwks_uri endpoint and use it to construct the RSA public key
    JWT_PUBLIC_KEY = RSAAlgorithm.from_jwk(json.dumps(oidc_jwks_uri["keys"][0]))
    # audience is oidc client id (can be array starting
    # https://github.com/vimalloc/flask-jwt-extended/issues/219)
    JWT_DECODE_AUDIENCE = ["rdmsvm-implicit-flow", "oidcdebugger-implicit-flow"]
    # name of token entry that will become distinct flask identity username
    # example 'sub'/'email'
    JWT_IDENTITY_CLAIM = os.environ.get("OIDC_USERNAME_CLAIM")


class TestingConfig(BaseConfig):
    """Testing configuration"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")
    ELASTICSEARCH_URL = None
    JWT_SECRET_KEY = 'super-secret'
    JWT_ALGORITHM = 'HS256'
    JWT_IDENTITY_CLAIM = "identity"
    JWT_DECODE_AUDIENCE = None


class ProductionConfig(BaseConfig):
    """Production configuration"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL")
