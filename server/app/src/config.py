import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
  SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret_key')
  DEBUG = False

class DevelopmentConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = 'postgres://postgres:postgres@localhost/dev'
  SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
  DEBUG = True
  TESTING = True
  SQLALCHEMY_DATABASE_URI = 'postgres://postgres:postgres@localhost/dev'
  PRESERVE_CONTEXT_ON_EXCEPTION = False
  SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
  DEBUG = False
  SQLALCHEMY_DATABASE_URI = 'postgres://postgres:postgres@localhost/dev'

config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY