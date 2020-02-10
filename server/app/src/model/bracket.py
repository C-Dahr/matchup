from enum import Enum
from .. import ma

class BracketSource(Enum):
  CHALLONGE = 'challonge'
  SMASHGG = 'smashgg'

class Bracket:
  def __init__(self, id, source, game_name, number_of_setups, number_of_players):
    self.id = id
    self.source = BracketSource(source).name # makes sure the source is a valid enum
    self.game_name = game_name
    self.number_of_setups = number_of_setups
    self.number_of_players = number_of_players

class BracketSchema(ma.Schema):
  class Meta:
    fields = ('id', 'source', 'game_name', 'number_of_setups', 'number_of_players')