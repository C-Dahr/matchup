import challonge
from ..model.player import Player, PlayerSchema
from ..model.bracket import Bracket, BracketSchema
from ..model.tables import BracketPlayers, ChallongePlayer

player_schema = PlayerSchema()
bracket_schema = BracketSchema()

def determine_priority_for_matches(matches_not_in_progress, bracket):
  for match in matches_not_in_progress:
    player1 = build_player_data(match['player1_id'], bracket)
    player2 = build_player_data(match['player2_id'], bracket)

    match['player1'] = player1
    match['player2'] = player2
    match['bracket'] = bracket_schema.jsonify(bracket).json
    match['priority'] = 0
  
  return matches_not_in_progress

def build_player_data(challonge_player_id, bracket):
  challonge_player = ChallongePlayer.query.get({'challonge_id':challonge_player_id, 'bracker_id':bracket.bracket_id})
  player = challonge_player.player
  bracket_player = BracketPlayers.query.get({'bracket_id':bracket.id, 'player_id':player.id})

  player_data = player_schema.jsonify(player).json
  player_data['name'] = bracket_player.name
  return player_data

def get_highest_priority_matches(matches_sorted_by_priority, bracket_setups):
  matches_called = []
  for match in matches_sorted_by_priority:
    if bracket_has_setups_available(match['bracket'], bracket_setups) and both_players_have_not_been_called(match, matches_called):
      take_setup_from_bracket(bracket_setups, match['bracket'])
      matches_called.append(match)
  return matches_called

def bracket_has_setups_available(bracket, bracket_setups):
  return bracket_setups[bracket['id']] > 0

def take_setup_from_bracket(bracket_setups, bracket):
  bracket_setups[bracket['id']] = bracket_setups[bracket['id']] - 1

def both_players_have_not_been_called(match, matches_called):
  player1 = match['player1']
  player2 = match['player2']
  for match in matches_called:
    if match_contains_player(match, player1) or match_contains_player(match, player2):
      return False
  return True

def match_contains_player(match, player):
  return match['player1']['id'] == player['id'] or match['player2']['id'] == player['id']