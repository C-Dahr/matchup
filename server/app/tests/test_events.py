from manage import app, db
import unittest
from flask_testing import TestCase
from flask import Flask
from app.src.config import basedir
from app.src.model.user import User
from app.src.model.event import Event
from werkzeug.security import generate_password_hash
import json
import base64
import pdb

BASE_URL = 'http://localhost:5000/event'
LOGIN_URL = 'http://localhost:5000/auth'
challonge_api_key = 'lDV85oOJLqA1ySxegdJQQcVghlA1bgWi3tUyOGNN'
bracket_1_id = 8061588
bracket_2_id = 8061653

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
    self.tk_valid_user = returned['token']
    self.headers = {'Content-Type': 'application/json', 'x-access-token': self.tk_valid_user}

  def tearDown(self):
    db.session.remove()
    db.drop_all()

class TestCreateEvent(BaseTestCase):
  def test_create_event(self):
    event_data = {
      'event_name': 'The Guard 22',
      'brackets': [
        {
          'bracket_id': bracket_1_id,
          'number_of_setups': 4
        },
        {
          'bracket_id': bracket_2_id,
          'number_of_setups': 5
        }
      ]
    }
    response = self.client.post(BASE_URL, json=event_data, headers=self.headers)
    event_returned = json.loads(response.data)
    primary_key = {
      'event_name': event_returned['event_name'],
      'user_id': event_returned['user_id']
    }
    event_from_db = Event.query.get(primary_key)
    self.assertEqual(event_data['event_name'], event_returned['event_name'], event_from_db.event_name)

  # def test_create_event_missing_fields(self):
  #   event_data = {
  #     'event_name': 'The Guard 22',
  #     'brackets': [
  #       {
  #         'bracket_id': 1
  #       },
  #       {
  #         'bracket_id': 2
  #       }
  #     ]
  #   }
  #   response = self.client.put(BASE_URL, json=event_data, headers=self.headers)
  #   self.assert400(response)

  # def test_create_event_invalid_bracket(self):
  #   event_data = {
  #     'event_name': 'The Guard 22',
  #     'brackets': [
  #       {
  #         'bracket_id': 1,
  #         'number_of_setups': 4
  #       },
  #       {
  #         'bracket_id': 2,
  #         'number_of_setups': 5
  #       }
  #     ]
  #   }
  #   response = self.client.put(BASE_URL, json=event_data, headers=self.headers)
  #   self.assert400(response)

  