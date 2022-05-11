from environs import Env

env = Env()
env.read_env()


class BaseConfig:
    """Base configuration"""

    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "top_secret"
    DEFAULT_POOL_TIMEOUT = 600
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


class DevelopmentConfig(BaseConfig):
    """Development configuration"""

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
    """Testing configuration"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = env("DATABASE_TEST_URL", None)
    ELASTICSEARCH_URL = None
    # https://github.com/jarus/flask-testing/issues/21
    # AssertionError: Popped wrong request context
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration"""

    SECRET_KEY = env("SECRET_KEY", "top_secret")
    SQLALCHEMY_DATABASE_URI = env("DATABASE_URL", None)
    ELASTICSEARCH_URL = env("ELASTICSEARCH_URL", None)
    OIDC_WELL_KNOWN_URL = env("WELL_KNOWN_URL", None)
    OIDC_USERDATA_IDENTITY_CLAIM = env("OIDC_USERNAME_CLAIM", "sub")
