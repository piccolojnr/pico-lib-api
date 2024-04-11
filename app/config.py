"""Config settings for for development, testing and production environments."""

import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()
POSTSQL_DB = os.environ.get("POSTSQL_DB")
POSTSQL_USER = os.environ.get("POSTSQL_USER")
POSTSQL_PASSWORD = os.environ.get("POSTSQL_PASSWORD")
POSTSQL_HOST = os.environ.get("POSTSQL_HOST")
POSTSQL_SSLMODE = os.environ.get("POSTSQL_SSLMODE")

HERE = Path(__file__).parent

POSTSQL_DEV = "postgresql://{username}:{password}@{host}:5433/{db}".format(
    username="postgres",
    password="hummer64",
    host="localhost",
    db="pico_library_db_dev",
)
POSTSQL_TEST = "postgresql://{username}:{password}@{host}:5433/{db}".format(
    username="postgres",
    password="hummer64",
    host="localhost",
    db="pico_library_db_test",
)
POSTSQL_PROD = (
    "postgresql://{username}:{password}@{host}/{db}?sslmode={sslmode}".format(
        username=POSTSQL_USER,
        password=POSTSQL_PASSWORD,
        host=POSTSQL_HOST,
        db=POSTSQL_DB,
        sslmode=POSTSQL_SSLMODE,
    )
)

MY_DOMAIN = os.environ.get("MY_DOMAIN")


class Config:
    """Base configuration."""

    BCRYPT_LOG_ROUNDS = 4

    TOKEN_EXPIRE_HOURS = 0
    TOKEN_EXPIRE_MINUTES = 0
    JWT_AUTHMAXAGE = 0
    JWT_REFRESHMAXAGE = 0

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SWAGGER_UI_DOC_EXPANSION = "list"
    RESTX_MASK_SWAGGER = False
    JSON_SORT_KEYS = False


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    JWT_AUTHMAXAGE = 5
    JWT_REFRESHMAXAGE = 10
    SQLALCHEMY_DATABASE_URI = POSTSQL_TEST


class DevelopmentConfig(Config):
    """Development configuration."""

    TOKEN_EXPIRE_MINUTES = 15
    JWT_AUTHMAXAGE = 900
    JWT_REFRESHMAXAGE = 3600
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", POSTSQL_DEV)
    SQLALCHEMY_DATABASE_URI = POSTSQL_TEST
    SECRET_KEY = os.getenv("SECRET_KEY")

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")


class ProductionConfig(Config):
    """Production configuration."""

    TOKEN_EXPIRE_HOURS = 1
    BCRYPT_LOG_ROUNDS = 13
    JWT_AUTHMAXAGE = 3600
    JWT_REFRESHMAXAGE = 604800
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", POSTSQL_PROD)
    PRESERVE_CONTEXT_ON_EXCEPTION = True
    SECRET_KEY = os.getenv("SECRET_KEY")

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")


ENV_CONFIG_DICT = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
)


def get_config(config_name):
    """Retrieve environment configuration settings."""
    return ENV_CONFIG_DICT.get(config_name, ProductionConfig)
