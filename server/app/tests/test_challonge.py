from manage import app, db
import unittest
from flask_testing import TestCase
from flask import Flask
from app.src.config import basedir
from app.src.model.user import User
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
    test_user = User('testuser', 'password', 'test@gmail.com', 'matchuptesting', challonge_api_key)
    self.test_user = test_user

    db.drop_all()
    db.create_all()
    db.session.add(self.test_user)
    db.session.commit()


  def tearDown(self):
    db.session.remove()
    db.drop_all()

class TestCredentials(BaseTestCase):
  def test_valid_credentials(self):
    data = '"testuser" : "password"'
    data = base64.b64encode(data.encode("utf-8"))
    datastr = str(data, 'utf-8')
    datastr = 'Basic ' + datastr
    self.headers = {'Content-Type': 'application/json', 'Authorization': datastr}
    response = self.client.post(LOGIN_URL, headers=self.headers)
    token = json.loads(response.data)
    token = token['token']
    self.headers = {'Content-Type': 'application/json', 'x-access-token': token}
    response = self.client.get(BASE_URL, json={"username": "matchuptesting"}, headers=self.headers)
    self.assert200(response)

  #def test_invalid_credentials(self):


