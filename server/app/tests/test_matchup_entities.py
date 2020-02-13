from manage import app, db
import unittest
from flask_testing import TestCase
from flask import Flask
from app.src.config import basedir
from app.src.model.user import User
from app.src.model.bracket import Bracket, BracketSchema
from app.src.model.match import Match
from app.src.model.player import Player, PlayerSchema
from app.src.model.event import Event
import json

bracket_schema = BracketSchema()
brackets_schema = BracketSchema(many=True)

player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)

class BaseTestCase(TestCase):
  def create_app(self):
    app.config.from_object('app.src.config.TestingConfig')
    return app
  
  def setUp(self):
    test_user = User('testuser', 'password', 'test@gmail.com', 'testuser', 'challonge123')
    self.test_user = test_user

    db.drop_all()
    db.create_all()
    db.session.add(self.test_user)
    db.session.commit()

  def tearDown(self):
    db.session.remove()
    db.drop_all()

class TestCreateEntities(BaseTestCase):
  def test_set_up_event(self):
    # create a bracket
    bracket = Bracket(1, "challonge", "Melee", 4)
    # create 2 players
    player1 = Player(1, "DieHard", [bracket.id], [2])
    player2 = Player(2, "Rice", [bracket.id], [4])
    # create a match between those players
    match = Match(1, player1.id, player2.id, 1, bracket.id, bracket.game_name)
    match.priority = 7
    # create an event 
    bracket_json = bracket_schema.jsonify(bracket)
    players_json = players_schema.jsonify([player1, player2])

    event = Event("The Guard 22", self.test_user.id, bracket_json.json)
    event.players = players_json.json
    event.matches = [match]
    db.session.add(event)
    db.session.commit()
    event_from_db = Event.query.get({'event_name': event.event_name, 'user_id': event.user_id})
    self.assertEquals(event, event_from_db)
