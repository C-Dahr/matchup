from manage import app, db
import unittest
from flask_testing import TestCase
from flask import Flask
from app.src.config import basedir
from app.src.model.user import User
from app.src.model.event import Event
from app.src.model.player import Player
from app.src.model.bracket import Bracket
from werkzeug.security import generate_password_hash
from app.src.controller import xor_crypt_string
from app.src.service.event_service import *
import json
import base64

BASE_URL = 'http://localhost:5000'
CREATE_EVENT_URL = BASE_URL + '/event'
LOGIN_URL = BASE_URL + '/auth'
PLAYER_URL = CREATE_EVENT_URL + '/players'
GET_EVENTS_URL = BASE_URL + '/user/events'
challonge_api_key = xor_crypt_string('lDV85oOJLqA1ySxegdJQQcVghlA1bgWi3tUyOGNN', encode=True)
bracket_1_id = 8061588
bracket_2_id = 8061653
bracket_3_id = 8176881
bracket_5_id = 8176890

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

    valid_credentials = base64.b64encode(b'testuser:password').decode('utf-8')
    response = self.client.post(LOGIN_URL, headers={'Authorization': 'Basic ' + valid_credentials})
    returned = json.loads(response.data)
    self.tk_valid_user = returned['token']
    self.headers = {'Content-Type': 'application/json', 'x-access-token': self.tk_valid_user}

    event_data = {
      'event_name': 'Test Event',
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
    response = self.client.post(CREATE_EVENT_URL, json=event_data, headers=self.headers)
    self.test_event = Event.query.get(json.loads(response.data)['id'])

  def tearDown(self):
    db.session.remove()
    db.drop_all()

class TestUserEvents(BaseTestCase):
  def test_get_user_events(self):
    NUMBER_OF_EVENTS = 1
    response = self.client.get(GET_EVENTS_URL, headers=self.headers)
    response_json = json.loads(response.data)
    self.assertEqual(len(response_json), NUMBER_OF_EVENTS)
