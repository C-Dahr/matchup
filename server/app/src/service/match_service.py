import challonge
import pdb
from ..model.match import Match
from ..model.player import Player, PlayerSchema
from ..model.bracket import Bracket, BracketSchema
from ..model.tables import BracketPlayers, ChallongePlayer

player_schema = PlayerSchema()
bracket_schema = BracketSchema()

def get_highest_priority_matches(event, bracket, matches_called):
  list_of_matches = challonge.matches.index(bracket.bracket_id, state='open')
  for match in list_of_matches:
    player1 = build_player_data(match['player1_id'], bracket)
    player2 = build_player_data(match['player2_id'], bracket)

    # if matches_called containts a match with either player id, set this matches priority to 0
    if either_player_has_been_called(player1, player2, matches_called):
      match['priority'] = -1
    else:
      match['player1'] = player1
      match['player2'] = player2
      match['bracket'] = bracket_schema.jsonify(bracket).json
      match['priority'] = 0
  
  list_of_matches = list(filter(lambda match: match['priority'] >= 0, list_of_matches))
  return list_of_matches[:bracket.number_of_setups]

def build_player_data(challonge_player_id, bracket):
  challonge_player = ChallongePlayer.query.filter_by(challonge_id=challonge_player_id).first()
  player = Player.query.get(challonge_player.player_id)
  bracket_player = BracketPlayers.query.get({'bracket_id':bracket.id, 'player_id':player.id})

  player_data = player_schema.jsonify(player).json
  player_data['name'] = bracket_player.name
  return player_data

def either_player_has_been_called(player1, player2, matches_called):
  for match in matches_called:
    if match_contains_player(match, player1) or match_contains_player(match, player2):
      return True
  return False

def match_contains_player(match, player):
  return match['player1']['id'] == player['id'] or match['player2']['id'] == player['id']