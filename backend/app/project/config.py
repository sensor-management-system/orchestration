# SPDX-FileCopyrightText: 2020 - 2023
# - Martin Abbrent <martin.abbrent@ufz.de>
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Dirk Ecker <d.ecker@fz-juelich.de>
# - Florian Gransee <florian.gransee@ufz.de>
# - Forschungszentrum Jülich GmbH (FZJ, https://fz-juelich.de)
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Config for the app."""

from environs import Env

env = Env()
env.read_env()


class BaseConfig:
    """Base configuration."""

    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "top_secret"
    DEFAULT_POOL_TIMEOUT = 600
    # This will help us to see exceptions on background task to be visible
    # in the logging at least.
    EXECUTOR_PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_POOL_TIMEOUT = env.int("POOL_TIMEOUT", DEFAULT_POOL_TIMEOUT)
    # name of token entry that will become distinct flask identity username
    # example in our case it is {'sub':'username@ufz.de'}
    JWT_IDENTITY_CLAIM = env("OIDC_USERNAME_CLAIM", "sub")
    # Hostname of a S3 service.
    # Minio's context root is '/' and this cannot be configured.
    # So we use two endpoints.
    MINIO_ENDPOINT = env(
        "MINIO_ENDPOINT", "minio:9000"
    )  # refer to docker container name
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
    IDL_URL = env("IDL_URL", None)
    CATCH_EXCEPTIONS = True
    INSTITUTE = env("INSTITUTE", "ufz")
    OIDC_TOKEN_CACHING_SECONDS = env.int("OIDC_TOKEN_CACHING_SECONDS", 600)
    PKCE_SCOPES = env("PKCE_SCOPES", "openid profile email auth_context")
    PKCE_CLIENT_ID = env("PKCE_CLIENT_ID", "rdmsms-pkce-flow")
    SMS_BACKEND_URL = env("SMS_BACKEND_URL", "https://localhost.localdomain")
    SMS_FRONTEND_URL = env("SMS_FRONTEND_URL", "https://localhost.localdomain")
    CV_URL = env("CV_URL", "https://localhost.localdomain/backend/api/v1")
    # PID service
    PID_SERVICE_URL = env(
        "PID_SERVICE_URL", "http://vm04.pid.gwdg.de:8081/handles/21.T11998/"
    )
    PID_SERVICE_USER = env("PID_SERVICE_USER", None)
    PID_SERVICE_PASSWORD = env("PID_SERVICE_PASSWORD", None)
    PID_SUFFIX = env("PID_SUFFIX", "SMS-STAGE")
    PID_PREFIX = env("PID_PREFIX", None)
    PID_CERT_FILE = env("PID_CERT_FILE", None)
    PID_CERT_KEY = env("PID_CERT_KEY", None)
    # Or, as an alternative b2inst.
    B2INST_URL = env("B2INST_URL", "https://b2inst-test.gwdg.de")
    B2INST_TOKEN = env("B2INST_TOKEN", "")
    B2INST_COMMUNITY = env("B2INST_COMMUNITY", "EUDAT")
    SMS_VERSION = env("SMS_VERSION", "develop")
    PROXY_NETLOC_BLOCKLIST = env.list("PROXY_NETLOC_BLOCKLIST", [])
    EXPORT_CONTROL_VO_LIST = env.list("EXPORT_CONTROL_VO_LIST", [])


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    SQLALCHEMY_DATABASE_URI = env("DATABASE_URL", None)
    ELASTICSEARCH_URL = env("ELASTICSEARCH_URL", None)
    OIDC_WELL_KNOWN_URL = env("WELL_KNOWN_URL", None)
    # The one claim that we want to use when extracting the
    # 'identity' from the answer of the get userinfo endpoint.
    # In case of the helmholtz AAI we use something like
    # 'eduperson_principal_name'.
    # For other IDPs we may use just the 'sub'.
    # (In case we talk with the helmholtz idp, we don't want to use the sub
    # (as this is just a UUID). Instead we want to use the
    # eduperson_principal_name (the form <username>@<institute>.de)).
    OIDC_USERDATA_IDENTITY_CLAIM = env("OIDC_USERNAME_CLAIM", "sub")


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = env("DATABASE_TEST_URL", None)
    ELASTICSEARCH_URL = None
    # https://github.com/jarus/flask-testing/issues/21
    # AssertionError: Popped wrong request context
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    INSTITUTE = None
    SQLALCHEMY_ENGINE_OPTIONS = {"connect_args": {"options": "-c timezone=utc"}}


class ProductionConfig(BaseConfig):
    """Production configuration."""

    SECRET_KEY = env("SECRET_KEY", "top_secret")
    SQLALCHEMY_DATABASE_URI = env("DATABASE_URL", None)
    ELASTICSEARCH_URL = env("ELASTICSEARCH_URL", None)
    OIDC_WELL_KNOWN_URL = env("WELL_KNOWN_URL", None)
    OIDC_USERDATA_IDENTITY_CLAIM = env("OIDC_USERNAME_CLAIM", "sub")
