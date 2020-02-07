from manage import app, db
import unittest
from flask_testing import TestCase
from flask import Flask
from app.src.config import basedir
from app.src.model.user import User
from werkzeug.security import generate_password_hash
import json
import base64

BASE_URL = 'http://localhost:5000/challonge'
LOGIN_URL = 'http://localhost:5000/auth'
challonge_api_key = 'lDV85oOJLqA1ySxegdJQQcVghlA1bgWi3tUyOGNN'

class BaseTestCase(TestCase):  
  def create_app(self):
    app.config.from_object('app.src.config.TestingConfig')
    return app

  def setUp(self):
    password = generate_password_hash('password')
    test_user = User('testuser', password, 'test@gmail.com', 'matchuptesting', challonge_api_key)
    self.test_user = test_user

    db.drop_all()
    db.create_all()
    db.session.add(self.test_user)
    db.session.commit()

    valid_credentials = base64.b64encode(b'testuser:password').decode('utf-8')
    response = self.client.post(LOGIN_URL, headers={'Authorization': 'Basic ' + valid_credentials})
    returned = json.loads(response.data)
    self.tk = returned['token']


  def tearDown(self):
    db.session.remove()
    db.drop_all()

class TestCredentials(BaseTestCase):
  def test_valid_credentials(self):
    response = self.client.get(BASE_URL, headers={'Content-Type': 'application/json', 'x-access-token': self.tk})
    self.assert200(response)

  #def test_invalid_credentials(self):


