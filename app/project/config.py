import os


class BaseConfig:
    """Base configuration"""

    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "top_secret"

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
    MINIO_SECURE = os.getenv("MINIO_SECURE", False)
    # (Optional) Region name of buckets in S3 service.
    REGION = os.getenv("REGION", None)
    # (Optional) Customized HTTP client.
    # learn more https://docs.min.io/docs/python-client-api-reference.html
    HTTP_CLIENT = os.getenv("HTTP_CLIENT", None)


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
