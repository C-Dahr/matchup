from manage import app, db
import unittest
from flask_testing import TestCase
from flask import Flask
from app.src.config import basedir
from app.src.model.user import User
from app.src.model.event import Event
from werkzeug.security import generate_password_hash
from app.src.controller import xor_crypt_string
import json
import base64

BASE_URL = 'http://localhost:5000/challonge'
BRACKET_URL = BASE_URL + '/bracket'
MATCHES_URL = BASE_URL + '/matches'
LOGIN_URL = 'http://localhost:5000/auth'
EVENT_URL = 'http://localhost:5000/event'
challonge_api_key = xor_crypt_string('lDV85oOJLqA1ySxegdJQQcVghlA1bgWi3tUyOGNN', encode=True)

b1_id = 8176881
b2_id = 8176886
b3_id = 8176890
b4_id = 8177036
b5_id = 8177044

class BaseTestCase(TestCase):  
  def create_app(self):
    app.config.from_object('app.src.config.TestingConfig')
    return app

  def setUp(self):
    password = generate_password_hash('password')
    test_user = User('testuser', password, 'test@gmail.com', 'matchuptesting', challonge_api_key)
    test_bad_user = User('baduser', password, 'badtest@gmail.com', 'matchup', challonge_api_key)
    self.test_bad_user = test_bad_user
    self.test_user = test_user

    db.drop_all()
    db.create_all()
    db.session.add(self.test_user)
    db.session.add(self.test_bad_user)
    db.session.commit()

    valid_credentials = base64.b64encode(b'testuser:password').decode('utf-8')
    response = self.client.post(LOGIN_URL, headers={'Authorization': 'Basic ' + valid_credentials})
    returned = json.loads(response.data)
    self.tk_valid_user = returned['token']
    self.headers = {'Content-Type': 'application/json', 'x-access-token': self.tk_valid_user}

    event1_data = {
      'event_name': 'Test Event 1',
      'brackets': [
        {
          'bracket_id': b1_id,
          'number_of_setups': 0
        },
        {
          'bracket_id': b2_id,
          'number_of_setups': 0
        }
      ]
    }

    event2_data = {
      'event_name': 'Test Event 1',
      'brackets': [
        {
          'bracket_id': b3_id,
          'number_of_setups': 0
        },
        {
          'bracket_id': b4_id,
          'number_of_setups': 0
        }
      ]
    }

    event3_data = {
      'event_name': 'Test Event 1',
      'brackets': [
        {
          'bracket_id': b3_id,
          'number_of_setups': 0
        },
        {
          'bracket_id': b5_id,
          'number_of_setups': 0
        }
      ]
    }

    response1 = self.client.post(EVENT_URL, json=event1_data, headers=self.headers)
    self.event1 = Event.query.get(json.loads(response1.data)['id'])

    response2 = self.client.post(EVENT_URL, json=event2_data, headers=self.headers)
    self.event2 = Event.query.get(json.loads(response2.data)['id'])

    response3 = self.client.post(EVENT_URL, json=event3_data, headers=self.headers)
    self.event3 = Event.query.get(json.loads(response3.data)['id'])


  def tearDown(self):
    db.session.remove()
    db.drop_all()

class TestMatches(BaseTestCase):
  def test_invalid_event(self):
    pass

  def test_event_not_owned_by_user(self):
    pass

class TestMathcesSetups(BaseTestCase):
  def test_more_setups_than_matches(self):
    pass

  def test_less_setups_than_matches(self):
    pass

  def test_no_setups_available(self):
    pass

  def test_no_setups_on_bracket(self):
    pass

  def test_some_setups_available(self):
    pass


class TestMatchesPlayerConflicts(BaseTestCase):
  def test_no_conflicts(self):
    pass

  def test_one_conflict(self):
    pass

  def test_two_conflicts(self):
    pass

class TestCredentials(BaseTestCase):
  def test_valid_credentials(self):
    response = self.client.get(BRACKET_URL, headers={'Content-Type': 'application/json', 'x-access-token': self.tk_valid_user})
    self.assert200(response)

  def test_invalid_credentials(self):
    invalid_credentials = base64.b64encode(b'baduser:password').decode('utf-8')
    response = self.client.post(LOGIN_URL, headers={'Authorization': 'Basic ' + invalid_credentials})
    returned = json.loads(response.data)
    tk = returned['token']
    response = self.client.get(BRACKET_URL, headers={'Content-Type': 'application/json', 'x-access-token': tk})
    self.assert401(response)