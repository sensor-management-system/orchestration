import json
import os

import requests
from jwt.algorithms import RSAAlgorithm


class OidcJwksConfig(object):
    _instance = None

    def __new__(cls, oidc_issuer_url, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, oidc_issuer_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # retrieve master openid-configuration endpoint for issuer realm
        self.oidc_config = requests.get(oidc_issuer_url, verify=False).json()
        # # retrieve data from jwks_uri endpoint
        self.oidc_jwks_uri = requests.get(self.oidc_config["jwks_uri"], verify=False).json()


def env_value_to_boolean(param):
    """
    Convert a string to boolean.
    :param param: str
    :return: boolean
    """
    if isinstance(param, str):
        _bool = param.lower() in ("true", 'yes', True)
        return _bool
    return param


def env_values_to_list(param):
    """
    Convert a string to a list.
    :param param:
    :return:
    """
    if isinstance(param, str):
        # create a list
        _list = param.split()
        return _list
    return param


class BaseConfig:
    """Base configuration"""

    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "top_secret"
    HTTP_ORIGINS = env_values_to_list(os.getenv("HTTP_ORIGINS", None))
    DEFAULT_POOL_TIMEOUT = 600
    SQLALCHEMY_POOL_TIMEOUT = os.environ.get("POOL_TIMEOUT", DEFAULT_POOL_TIMEOUT)
    # Hostname of a S3 service.
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "172.16.238.10:9000")
    # Access key (aka user ID) of your account in S3 service.
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minio")
    # Secret Key (aka password) of your account in S3 service.
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minio123")
    # (Optional) Flag to indicate to use secure (TLS) connection to S3 service or not.
    # False for local testing
    MINIO_SECURE = env_value_to_boolean(os.getenv("MINIO_SECURE", False))
    # (Optional) Region name of buckets in S3 service.
    MINIO_REGION = os.getenv("MINIO_REGION", None)
    # (Optional) Customized HTTP client.
    # learn more https://docs.min.io/docs/python-client-api-reference.html
    MINIO_HTTP_CLIENT = os.getenv("MINIO_HTTP_CLIENT", None)
    MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "sms")
    # ALLOWED_EXTENSIONS = env_values_to_list(os.getenv("ALLOWED_EXTENSIONS"))


class DevelopmentConfig(BaseConfig):
    """Development configuration"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL")
    # Setup Token Verification
    # force use of RS265
    JWT_ALGORITHM = "RS256"
    oidc_issuer_url = os.environ.get("WELL_KNOWN_URL")
    oidc_jwks_uri = OidcJwksConfig(oidc_issuer_url).oidc_jwks_uri
    # retrieve first jwk entry from jwks_uri endpoint and use it to construct the RSA public key
    JWT_PUBLIC_KEY = RSAAlgorithm.from_jwk(json.dumps(oidc_jwks_uri["keys"][0]))
    # audience is oidc client id (can be array starting
    # https://github.com/vimalloc/flask-jwt-extended/issues/219)
    JWT_DECODE_AUDIENCE = ["rdmsvm-implicit-flow", "oidcdebugger-implicit-flow"]
    # name of token entry that will become distinct flask identity username
    # example in our case it is {'sub':'username@ufz.de'}
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
