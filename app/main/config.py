from decouple import config
from main.db.database import db


class Config:
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class FeatureTestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL', default='localhost')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = dict(
    development=DevelopmentConfig,
    featureTest=FeatureTestingConfig,
    production=ProductionConfig
)
