import json
import os

import requests
from cachetools import cached, TTLCache
from jwt.algorithms import RSAAlgorithm


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
    SQLALCHEMY_POOL_TIMEOUT = os.environ.get("POOL_TIMEOUT", DEFAULT_POOL_TIMEOUT)
    # example in our case it is {'sub':'username@ufz.de'}
    JWT_IDENTITY_CLAIM = os.environ.get("OIDC_USERNAME_CLAIM")


class DevelopmentConfig(BaseConfig):
    """Development configuration"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL")

    # We can use the OIDC_JWT_SERVICE to query the latest information
    # from the IDP.
    OIDC_JWT_SERVICE = OidcJwtService(os.environ.get("WELL_KNOWN_URL"))
    JWT_ALGORITHM = OIDC_JWT_SERVICE.get_jwt_algorithm()
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


class TestingConfig(BaseConfig):
    """Testing configuration"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")
    ELASTICSEARCH_URL = None
    JWT_SECRET_KEY = "super-secret"
    JWT_ALGORITHM = "HS256"
    JWT_DECODE_AUDIENCE = "SMS"


class ProductionConfig(BaseConfig):
    """Production configuration"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL")
