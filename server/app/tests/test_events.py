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

BASE_URL = 'http://localhost:5000/event'
LOGIN_URL = 'http://localhost:5000/auth'
PLAYER_URL = BASE_URL + '/players'
challonge_api_key = xor_crypt_string('lDV85oOJLqA1ySxegdJQQcVghlA1bgWi3tUyOGNN', encode=True)
bracket_1_id = 8061588
bracket_2_id = 8061653
bracket_3_id = 8176881
bracket_4_id = 8176886
bracket_5_id = 8176890
cameron_TestTournament_id = 1
danny_TestTournament_id = 2
tayler_TestTournament_id = 3
zach_TestTournament_id = 3
danny_Test2_id = 5
player2_Test2_id = 6
player3_Test2_id = 7
player4_Test2_id = 8
danny_merged_TestTournament_id = 13

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

    extra_test_user = User('extratestuser', password, 'extra@gmail.com', 'matchup', challonge_api_key)
    db.session.add(extra_test_user)
    db.session.commit()

    valid_credentials = base64.b64encode(b'extratestuser:password').decode('utf-8')
    login_response = self.client.post(LOGIN_URL, headers={'Authorization': 'Basic ' + valid_credentials})
    returned = json.loads(login_response.data)
    self.tk_valid_user_2 = returned['token']
    self.headers_2 = {'Content-Type': 'application/json', 'x-access-token': self.tk_valid_user_2}

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
    response = self.client.post(BASE_URL, json=event_data, headers=self.headers)
    self.test_event = Event.query.get(json.loads(response.data)['id'])

    event_data = {
      'event_name': 'Test Event 2',
      'brackets': [
        {
          'bracket_id': bracket_3_id,
          'number_of_setups': 4
        },
        {
          'bracket_id': bracket_5_id,
          'number_of_setups': 5
        }
      ]
    } 
    response = self.client.post(BASE_URL, json=event_data, headers=self.headers)
    self.test_event_2 = Event.query.get(json.loads(response.data)['id'])

  def tearDown(self):
    db.session.remove()
    db.drop_all()

class TestCreateEvent(BaseTestCase):
  def test_create_event(self):
    event_data = {
      'event_name': 'The Guard 22',
      'brackets': [
        {
          'bracket_id': bracket_3_id,
          'number_of_setups': 4
        },
        {
          'bracket_id': bracket_4_id,
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
    new_number_of_setups = 7
    event_data = {
      'event_id': self.test_event.id,
      'event_name': 'Updated Test Event',
      'brackets': [
        {
          'bracket_id': bracket_1_id,
          'number_of_setups': new_number_of_setups
        },
        {
          'bracket_id': bracket_2_id,
          'number_of_setups': new_number_of_setups
        }
      ]
    }
    response = self.client.put(BASE_URL, json=event_data, headers=self.headers)
    event_returned = json.loads(response.data)
    event_from_db = Event.query.get(event_returned['id'])
    self.assertEqual(event_data['event_name'], event_returned['event_name'], event_from_db.event_name)

    bracket1 = Bracket.query.filter_by(bracket_id=bracket_1_id, event_id=event_from_db.id).first()
    bracket2 = Bracket.query.filter_by(bracket_id=bracket_2_id, event_id=event_from_db.id).first()
    self.assertEqual(bracket1.number_of_setups, new_number_of_setups)
    self.assertEqual(bracket2.number_of_setups, new_number_of_setups)

  def test_update_event_invalid_event_id(self):
    new_number_of_setups = 7
    event_data = {
      'event_id': -1,
      'event_name': 'Updated Test Event',
      'brackets': [
        {
          'bracket_id': bracket_1_id,
          'number_of_setups': new_number_of_setups
        },
        {
          'bracket_id': bracket_2_id,
          'number_of_setups': new_number_of_setups
        }
      ]
    }
    response = self.client.put(BASE_URL, json=event_data, headers=self.headers)
    self.assert404(response)

  def test_update_event_missing_fields(self):
    event_data = {
      'event_id': self.test_event.id,
      'event_name': 'Updated Test Event',
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
      'event_id': self.test_event.id,
      'event_name': 'Updated Test Event',
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

class TestGetPlayers(BaseTestCase):
  def test_user_does_not_own_event(self):
    data = {
      'event_id': self.test_event.id,
    }
    response = self.client.get(PLAYER_URL, json=data, headers=self.headers_2)
    self.assert401(response)
  
  def test_valid_get(self):
    data = {
      'event_id': self.test_event_2.id,
    }
    response = self.client.get(PLAYER_URL, json=data, headers=self.headers)
    lists_returned = json.loads(response.data)
    self.assertEqual(len(lists_returned[str(bracket_3_id)]), 0)
    self.assertEqual(len(lists_returned[str(bracket_5_id)]), 4)
    self.assertEqual(len(lists_returned['both_brackets']), 4)
    self.assert200(response)

class TestMergePlayers(BaseTestCase):
  def test_user_does_not_own_event(self):
    player_data = {
      'event_id': self.test_event.id,
      'players' : [
        {
          'id_1': tayler_TestTournament_id,
          'id_2': player2_Test2_id
        }
      ]
    }
    response = self.client.post(PLAYER_URL, json=player_data, headers=self.headers_2)
    self.assert401(response)

  def test_merge_valid_players(self):
    player_data = {
      'event_id': self.test_event.id,
      'players' : [
        {
          'id_1': tayler_TestTournament_id,
          'id_2': player2_Test2_id
        }
      ]
    }
    response = self.client.post(PLAYER_URL, json=player_data, headers=self.headers)
    old_player1 = Player.query.get(tayler_TestTournament_id)
    old_player2 = Player.query.get(player2_Test2_id)
    self.assertEqual(None, old_player1, old_player2)
    self.assert200(response)

  def test_merge_multiple_valid_players(self):
    player_data = {
      'event_id': self.test_event.id,
      'players' : [
        {
          'id_1': cameron_TestTournament_id,
          'id_2': player3_Test2_id
        },
        {
          'id_1': zach_TestTournament_id,
          'id_2': player4_Test2_id
        }
      ]
    }
    response = self.client.post(PLAYER_URL, json=player_data, headers=self.headers)
    old_player1 = Player.query.get(cameron_TestTournament_id)
    old_player2 = Player.query.get(player3_Test2_id)
    old_player3 = Player.query.get(zach_TestTournament_id)
    old_player4 = Player.query.get(player4_Test2_id)
    self.assertEqual(None, old_player1, old_player2)
    self.assertEqual(None, old_player3, old_player4)
    self.assert200(response)

  def test_merge_invalid_event_id(self):
    player_data = {
      'event_id': 13,
      'players' : [
        {
          'id_1': tayler_TestTournament_id,
          'id_2': player2_Test2_id
        }
      ]
    }
    response = self.client.post(PLAYER_URL, json=player_data, headers=self.headers)
    self.assert404(response)

  def test_merge_players_same_bracket(self):
    player_data = {
      'event_id': self.test_event.id,
      'players' : [
        {
          'id_1': player2_Test2_id,
          'id_2': player3_Test2_id
        }
      ]
    }
    response = self.client.post(PLAYER_URL, json=player_data, headers=self.headers)
    self.assert400(response)

  def test_merge_player_twice(self):
    player_data = {
      'event_id': self.test_event.id,
      'players' : [
        {
          'id_1': danny_merged_TestTournament_id,
          'id_2': player3_Test2_id
        }
      ]
    }
    response = self.client.post(PLAYER_URL, json=player_data, headers=self.headers)
    self.assert400(response)

  def test_merge_nonexistent_players(self):
    player_data = {
      'event_id': self.test_event.id,
      'players' : [
        {
          'id_1': 200,
          'id_2': player2_Test2_id
        }
      ]
    }
    response = self.client.post(PLAYER_URL, json=player_data, headers=self.headers)
    self.assert400(response)

  def test_merge_from_wrong_event(self):
    event_data = {
      'event_name': 'The Guard 22',
      'brackets': [
        {
          'bracket_id': bracket_3_id,
          'number_of_setups': 4
        },
        {
          'bracket_id': bracket_4_id,
          'number_of_setups': 5
        }
      ]
    }  
    self.client.post(BASE_URL, json=event_data, headers=self.headers)
    player_data = {
      'event_id': self.test_event.id,
      'players' : [
        {
          'id_1': 19,
          'id_2': 20
        }
      ]
    }
    response = self.client.post(PLAYER_URL, json=player_data, headers=self.headers)
    self.assert400(response)