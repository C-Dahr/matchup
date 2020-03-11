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
import challonge

BASE_URL = 'http://localhost:5000/challonge'
MATCH_URL = BASE_URL + '/match/start'
LOGIN_URL = 'http://localhost:5000/auth'
EVENT_URL = 'http://localhost:5000/event'
challonge_api_key = xor_crypt_string('lDV85oOJLqA1ySxegdJQQcVghlA1bgWi3tUyOGNN', encode=True)

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

    event_data = {
      'event_name': 'Test Event',
      'brackets': [
        {
          'bracket_id': bracket_1_id,
          'number_of_setups': 0
        },
        {
          'bracket_id': bracket_2_id,
          'number_of_setups': 0
        }
      ]
    }

    response = self.client.post(EVENT_URL, json=event_data, headers=self.headers)
    self.event = Event.query.get(json.loads(response.data)['id'])

    challonge.set_credentials(self.test_user.challonge_username, xor_crypt_string(self.test_user.api_key, decode=True))
    
    # reset bracket
    challonge.tournaments.reset(bracket_1_id)
    challonge.tournaments.start(bracket_1_id)

    self.matches_available_bracket_1 = challonge.matches.index(bracket_1_id, state='open')
    self.num_matches = len(self.matches_available_bracket_1)
    self.match_to_test = self.matches_available_bracket_1[0]

  def tearDown(self):
    db.session.remove()
    db.drop_all()

    # reset bracket
    challonge.tournaments.reset(bracket_1_id)
    challonge.tournaments.start(bracket_1_id)

class TestMatchesMarkInProgress(BaseTestCase):
  def test_mark_match_as_in_progress(self):
    # make sure the match to test is not in progress before starting
    self.assertTrue(self.match_to_test['underway_at'] is None)
    match_data = {
      'event_id': self.event.id,
      'bracket_id': self.event.brackets[0].id,
      'match_id': self.match_to_test['id']
    }
    response = self.client.put(MATCH_URL, json=match_data, headers=self.headers)
    self.assertTrue(response.json['match']['underway_at'] is not None)

  def test_mark_in_progress_user_does_not_own_event(self):
    password = generate_password_hash('password')
    extra_test_user = User('extratestuser', password, 'extra@gmail.com', 'matchup', challonge_api_key)
    db.session.add(extra_test_user)
    db.session.commit()

    valid_credentials = base64.b64encode(b'extratestuser:password').decode('utf-8')
    login_response = self.client.post(LOGIN_URL, headers={'Authorization': 'Basic ' + valid_credentials})
    returned = json.loads(login_response.data)
 
    match_data = {
      'event_id': self.event.id,
      'bracket_id': self.event.brackets[0].id,
      'match_id': self.match_to_test['id']
    }

    response = self.client.put(MATCH_URL, json=match_data, headers={'Content-Type': 'application/json', 'x-access-token': returned['token']})
    self.assert401(response)
