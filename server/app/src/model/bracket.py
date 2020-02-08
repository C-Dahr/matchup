from enum import Enum
class BracketSource(Enum):
  CHALLONGE = 'challonge'
  SMASHGG = 'smashgg'

class Bracket:
  def __init__(self, id, source, game_name, number_of_setups, number_of_players):
    self.id = id
    self.source = BracketSource(source)
    self.game_name = game_name
    self.number_of_setups = number_of_setups
    self.number_of_players = number_of_players
