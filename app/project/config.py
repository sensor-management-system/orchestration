import json
import os

import requests
from cachetools import cached, TTLCache
from environs import Env
from jwt.algorithms import RSAAlgorithm

env = Env()
env.read_env()


class OidcJwtService:
    """Helper class to access the IDP."""

    def __init__(self, oidc_issuer_url):
        """Init the object from oidc_issuer url."""
        self.oidc_issuer_url = oidc_issuer_url

    def get_jwt_algorithm(self):
        """Return the JWT algorithm, so that we can set it to JWT_ALGORITHM."""
        # Currently we want to force the use of RS256
        return "RS256"

    def _get_oidc_config(self):
        resp = requests.get(self.oidc_issuer_url, verify=True)
        resp.raise_for_status()
        oidc_config = resp.json()
        return oidc_config

    def _get_jwks_config(self):
        oidc_config = self._get_oidc_config()
        jwks_uri = oidc_config["jwks_uri"]
        resp = requests.get(jwks_uri, verify=True)
        resp.raise_for_status()
        jwks_config = resp.json()
        return jwks_config

    # Cache the content for 10 minutes
    @cached(cache=TTLCache(maxsize=1, ttl=600))
    def get_jwt_public_key(self):
        """Return the JWT public key, so that we can se it to JWT_PUBLIC_KEY."""
        jwks_config = self._get_jwks_config()
        return RSAAlgorithm.from_jwk(json.dumps(jwks_config["keys"][0]))


class BaseConfig:
    """Base configuration"""

    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "top_secret"
    DEFAULT_POOL_TIMEOUT = 600
    SQLALCHEMY_POOL_TIMEOUT = env.int("POOL_TIMEOUT", DEFAULT_POOL_TIMEOUT)
    JWT_IDENTITY_CLAIM = env("OIDC_USERNAME_CLAIM")
    # Hostname of a S3 service.
    # Minio's context root is '/' and this cannot be configured.
    # So we use two endpoints.
    MINIO_ENDPOINT = env("MINIO_ENDPOINT", "minio:9000")  # refer to docker container name
    DOWNLOAD_ENDPOINT = env("DOWNLOAD_ENDPOINT", "localhost:9000")
    # Access key (aka user ID) of your account in S3 service.
    MINIO_ACCESS_KEY = env("MINIO_ACCESS_KEY", "minio")
    # Secret Key (aka password) of your account in S3 service.
    MINIO_SECRET_KEY = env("MINIO_SECRET_KEY", "minio123")
    # (Optional) Flag to indicate to use secure (TLS) connection to S3 service or not.
    # False for local testing
    MINIO_SECURE = env.bool("MINIO_SECURE", False)
    # (Optional) Region name of buckets in S3 service.
    MINIO_REGION = env("MINIO_REGION", None)
    # (Optional) Customized HTTP client.
    # learn more https://docs.min.io/docs/python-client-api-reference.html
    MINIO_HTTP_CLIENT = env("MINIO_HTTP_CLIENT", None)
    MINIO_BUCKET_NAME = env("MINIO_BUCKET_NAME", "sms-attachments")
    ALLOWED_MIME_TYPES = env.list("ALLOWED_MIME_TYPES", [])
    SMS_IDL_TOKEN = env("SMS_IDL_TOKEN", None)
    IDL_URL = env("IDL_URL", "http://172.21.0.11:80/dataprojects/api/user_accounts")
    CATCH_EXCEPTIONS = True


class DevelopmentConfig(BaseConfig):
    """Development configuration"""

    SQLALCHEMY_DATABASE_URI = env("DATABASE_URL", None)
    ELASTICSEARCH_URL = env("ELASTICSEARCH_URL", None)
    # We can use the OIDC_JWT_SERVICE to query the latest information
    # from the IDP.
    OIDC_JWT_SERVICE = OidcJwtService(os.environ.get("WELL_KNOWN_URL"))
    JWT_ALGORITHM = OIDC_JWT_SERVICE.get_jwt_algorithm()
    # retrieve first jwk entry from jwks_uri endpoint and use it to construct the RSA public key
    JWT_PUBLIC_KEY = OIDC_JWT_SERVICE.get_jwt_public_key()
    # audience is oidc client id (can be array starting
    # https://github.com/vimalloc/flask-jwt-extended/issues/219)
    # GFZ: Currently for the idp-dev the aud field and the client id seems to
    # be the very same values, so we want it to be part of the JWT_DECODE_AUDIENCE
    # that we trust.
    OIDC_CLIENT_IDS = os.environ.get("OIDC_CLIENT_IDS", "").split(" ")
    JWT_DECODE_AUDIENCE = ["rdmsvm-implicit-flow"]
    if OIDC_CLIENT_IDS:
        for client_id in OIDC_CLIENT_IDS:
            JWT_DECODE_AUDIENCE.append(client_id)
    # name of token entry that will become distinct flask identity username
    # example in our case it is {'sub':'username@ufz.de'}
    JWT_IDENTITY_CLAIM = env("OIDC_USERNAME_CLAIM", "sub")


class TestingConfig(BaseConfig):
    """Testing configuration"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = env("DATABASE_TEST_URL", None)
    ELASTICSEARCH_URL = None
    JWT_SECRET_KEY = "super-secret"
    JWT_ALGORITHM = "HS256"
    JWT_DECODE_AUDIENCE = "SMS"


class ProductionConfig(BaseConfig):
    """Production configuration"""

    SECRET_KEY = env("SECRET_KEY", "top_secret")
    SQLALCHEMY_DATABASE_URI = env("DATABASE_URL", None)
    ELASTICSEARCH_URL = env("ELASTICSEARCH_URL", None)
    OIDC_JWT_SERVICE = OidcJwtService(env("WELL_KNOWN_URL"))
    JWT_ALGORITHM = OIDC_JWT_SERVICE.get_jwt_algorithm()
    # retrieve first jwk entry from jwks_uri endpoint and use it to construct the RSA public key
    JWT_PUBLIC_KEY = OIDC_JWT_SERVICE.get_jwt_public_key()
    # For production we only want to have one audience that should be allowed
    JWT_DECODE_AUDIENCE = [env("OIDC_CLIENT_ID", None)]
    JWT_IDENTITY_CLAIM = env("OIDC_USERNAME_CLAIM", "sub")
