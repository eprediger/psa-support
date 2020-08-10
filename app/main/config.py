from decouple import config
import os

class Config:
    pass


class DevelopmentConfig(Config):
    DEBUG = True
#    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class FeatureTestingConfig(Config):
    DEBUG = True
#    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgres://odgquqttvlwybb:ff7f6c568bd3bbe6efa4514ec3fe892350f7a4386f1f1d2fd26ce6acda5dbd7e@ec2-52-204-20-42.compute-1.amazonaws.com:5432/d998qs20a58aqc'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = dict(
    development=DevelopmentConfig,
    featureTest=FeatureTestingConfig,
    production=ProductionConfig
)
