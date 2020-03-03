from manage import app, db
import unittest
from flask_testing import TestCase
from flask import Flask
from app.src.config import basedir
from app.src.model.user import User
from app.src.model.event import Event
from werkzeug.security import generate_password_hash
from app.src.controller import xor_crypt_string
from app.src.service.event_service import *
import json
import base64

BASE_URL = 'http://localhost:5000/event'
LOGIN_URL = 'http://localhost:5000/auth'
challonge_api_key = xor_crypt_string('lDV85oOJLqA1ySxegdJQQcVghlA1bgWi3tUyOGNN', encode=True)
bracket_1_id = 8061588
bracket_2_id = 8061653

class BaseTestCase(TestCase):  
  def create_app(self):
    app.config.from_object('app.src.config.TestingConfig')
    return app

  def setUp(self):
    db.drop_all()
    db.create_all()
    
    password = generate_password_hash('password')
    test_user = User('testuser', password, 'test@gmail.com', 'matchuptesting', challonge_api_key)
    self.test_user = test_user
    db.session.add(self.test_user)
    db.session.commit()
    
    test_event = Event('Test Event', test_user.id)
    self.test_event = test_event
    db.session.add(self.test_event)
    db.session.commit()

    bracket_data = {
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
    list_of_brackets = get_brackets_from_request(bracket_data['brackets'], test_event)
    for bracket in list_of_brackets:
        get_players_from_bracket(bracket)
        bracket.number_of_players = len(bracket.players)

    get_duplicate_players(list_of_brackets)
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
    event_from_db = Event.query.get(event_returned['id'])
    self.assertEqual(event_data['event_name'], event_returned['event_name'], event_from_db.event_name)

  def test_create_event_missing_fields(self):
    event_data = {
      'event_name': 'The Guard 22',
      'brackets': [
        {
          'bracket_id': 1
        },
        {
          'bracket_id': 2
        }
      ]
    }
    response = self.client.post(BASE_URL, json=event_data, headers=self.headers)
    self.assert400(response)

  def test_create_event_invalid_bracket(self):
    event_data = {
      'event_name': 'The Guard 22',
      'brackets': [
        {
          'bracket_id': -1,
          'number_of_setups': 4
        },
        {
          'bracket_id': -2,
          'number_of_setups': 5
        }
      ]
    }
    response = self.client.post(BASE_URL, json=event_data, headers=self.headers)
    # pychallonge throws a 401 if it doesn't receive anything back
    self.assert401(response)

class TestUpdateEvent(BaseTestCase):
  def test_update_event(self):
    event_data = {
      'event_name': 'Test Event',
      'brackets': [
        {
          'bracket_id': bracket_1_id,
          'number_of_setups': 7
        },
        {
          'bracket_id': bracket_2_id,
          'number_of_setups': 7
        }
      ]
    }
    response = self.client.put(BASE_URL, json=event_data, headers=self.headers)
    event_returned = json.loads(response.data)
    event_from_db = Event.query.get(event_returned['id'])
    self.assertEqual(event_data['event_name'], event_returned['event_name'], event_from_db.event_name)

  def test_update_event_missing_fields(self):
    event_data = {
      'event_name': 'Test Event',
      'brackets': [
        {
          'bracket_id': 1
        },
        {
          'bracket_id': 2
        }
      ]
    }
    response = self.client.put(BASE_URL, json=event_data, headers=self.headers)
    self.assert400(response)

  def test_update_event_invalid_bracket(self):
    event_data = {
      'event_name': 'Test Event',
      'brackets': [
        {
          'bracket_id': -1,
          'number_of_setups': 4
        },
        {
          'bracket_id': -2,
          'number_of_setups': 5
        }
      ]
    }
    response = self.client.put(BASE_URL, json=event_data, headers=self.headers)
    self.assert400(response)

class TestObjectCreation(BaseTestCase):
  def test_brackets_in_db(self):
    self.assertEqual(self.test_event.brackets[0].bracket_id, bracket_1_id)
    self.assertEqual(self.test_event.brackets[1].bracket_id, bracket_2_id)
    
  def test_players_in_db(self):
    self.assertEqual(len(self.test_event.brackets[0].players), 4)
    self.assertEqual(len(self.test_event.brackets[1].players), 8)
    self.assertEqual(len(Player.query.all()), 11)