from enum import Enum
from .. import db, ma
from flask import jsonify
from .tables import bracket_players

class BracketSource(Enum):
  CHALLONGE = 'challonge'
  SMASHGG = 'smashgg'

class Bracket(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  bracket_id = db.Column(db.Integer, nullable=False)
  source = db.Column(db.String(100), nullable=False)
  game_name = db.Column(db.String(100), nullable=False)
  number_of_setups = db.Column(db.Integer, nullable=False)
  number_of_players = db.Column(db.Integer, nullable=False)
  players = db.relationship("Player", secondary=bracket_players)

  def __init__(self, id, source, game_name, number_of_setups):
    self.bracket_id = id
    self.source = BracketSource(source).name # makes sure the source is a valid enum
    self.game_name = game_name
    self.number_of_setups = number_of_setups
    self.number_of_players = 0

class BracketSchema(ma.Schema):
  class Meta:
    fields = ('id', 'source', 'game_name', 'number_of_setups', 'number_of_players')
