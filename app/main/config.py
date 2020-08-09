from decouple import config


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
    SQLALCHEMY_DATABASE_URI = 'postgres://gengtoeqfhubby:1fd0821b236725b9d293caf66ab67ee51f57d4ad794eb8af1f75ce15514a42f7@ec2-34-200-15-192.compute-1.amazonaws.com:5432/da0s86t38gvpk7'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = dict(
    development=DevelopmentConfig,
    featureTest=FeatureTestingConfig,
    production=ProductionConfig
)
