import os
import unittest
from flask import current_app
from flask_testing import TestCase
from manage import app
from app.src.config import basedir

class TestDevelopmentConfig(TestCase):
  def create_app(self):
    app.config.from_object('app.src.config.DevelopmentConfig')
    return app

  def test_app_is_development(self):
    self.assertFalse(app.config['SECRET_KEY'] is 'my_key')
    self.assertTrue(app.config['DEBUG'] is True)
    self.assertFalse(current_app is None)
    self.assertTrue(
        app.config['SQLALCHEMY_DATABASE_URI'] == 'postgres://postgres:postgres@localhost/dev'
    )

class TestTestingConfig(TestCase):
  def create_app(self):
    app.config.from_object('app.src.config.TestingConfig')
    return app

  def test_app_is_testing(self):
    self.assertFalse(app.config['SECRET_KEY'] is 'my_key')
    self.assertTrue(app.config['DEBUG'])
    self.assertTrue(
        app.config['SQLALCHEMY_DATABASE_URI'] == 'postgres://postgres:postgres@localhost/dev'
    )

class TestProductionConfig(TestCase):
  def create_app(self):
    app.config.from_object('app.src.config.ProductionConfig')
    return app

  def test_app_is_production(self):
    self.assertTrue(app.config['DEBUG'] is False)
    self.assertTrue(
        app.config['SQLALCHEMY_DATABASE_URI'] == 'postgres://postgres:postgres@localhost/dev'
    )

if __name__ == '__main__':
    unittest.main()