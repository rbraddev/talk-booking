import os

import boto3


class ProductionConfig:
    DEBUG = False
    TESTING = False
    APP_ENVIRONMENT = "production"
    _SQLMODEL_DATABASE_URI = None

    @property
    def SQLMODEL_DATABASE_URI(self):
        if self._SQLMODEL_DATABASE_URI is None:
            self._SQLMODEL_DATABASE_URI = boto3.client(
                "secretsmanager"
            ).get_secret_value(SecretId=f"db-connection-string-{self.APP_ENVIRONMENT}")["SecretString"]

        return self._SQLMODEL_DATABASE_URI


class DevelopmentConfig(ProductionConfig):
    DEBUG = True
    APP_ENVIRONMENT = "development"


class TestConfig(ProductionConfig):
    DEBUG = True
    TESTING = True
    APP_ENVIRONMENT = "local"
    _SQLMODEL_DATABASE_URI = None

    @property
    def SQLMODEL_DATABASE_URI(self):
        return "postgresql://app:talkbooking@postgres:5432/talkbookingtest"


class LocalTestConfig(ProductionConfig):
    DEBUG = True
    APP_ENVIRONMENT = "local"
    _SQLMODEL_DATABASE_URI = None

    @property
    def SQLMODEL_DATABASE_URI(self):
        return "postgresql://app:talkbooking@localhost:5432/talkbooking_test"


class LocalConfig(ProductionConfig):
    DEBUG = True
    APP_ENVIRONMENT = "local"
    _SQLMODEL_DATABASE_URI = None

    @property
    def SQLMODEL_DATABASE_URI(self):
        return "postgresql://app:talkbooking@localhost:5432/talkbooking"


CONFIGS = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "test": TestConfig,
    "local_test": LocalTestConfig,
}


def load_config():
    """
    Load config based on environment
    :return:
    """

    return CONFIGS.get(os.getenv("APP_ENVIRONMENT"), LocalConfig)()
