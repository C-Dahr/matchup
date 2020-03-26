import challonge
from ..model.player import Player, PlayerSchema
from ..model.bracket import Bracket, BracketSchema
from ..model.tables import BracketPlayers, ChallongePlayer
import statistics

player_schema = PlayerSchema()
bracket_schema = BracketSchema()

player_overlap_priority_constant = 5
round_priority_constant = 2

def determine_priority_for_matches(matches_not_in_progress, bracket):
  average_round = get_mean_match_round(matches_not_in_progress)
  for match in matches_not_in_progress:
    player1_data, player1 = build_player_data(match['player1_id'], bracket)
    player2_data, player2 = build_player_data(match['player2_id'], bracket)

    match['player1'] = player1_data
    match['player2'] = player2_data
    match['bracket'] = bracket_schema.jsonify(bracket).json
    match['priority'] = calculate_match_priority(match, player1, player2, average_round)
  
  return matches_not_in_progress

def build_player_data(challonge_player_id, bracket):
  challonge_player = ChallongePlayer.query.get({'challonge_id':challonge_player_id, 'bracket_id':bracket.bracket_id})
  player = challonge_player.player
  bracket_player = BracketPlayers.query.get({'bracket_id':bracket.id, 'player_id':player.id})

  player_data = player_schema.jsonify(player).json
  player_data['name'] = bracket_player.name
  return player_data, player

def get_mean_match_round(matches):
  rounds = []
  for match in matches:
    rounds.append(match['round'])
  if len(rounds) != 0:
    return statistics.mean(rounds)
  else:
    -1

def calculate_match_priority(match, player1, player2, average_round):
  match_priority =  get_player_priority(player1) + get_player_priority(player2)
  match_priority += get_bracket_priority(match)
  match_priority += get_round_priority(match['round'], average_round)
  return match_priority

def get_player_priority(player):
  # 1 bracket: priorty = 0, 2 brackets: priority = 5
  return (len(player.brackets) - 1) * player_overlap_priority_constant

def get_bracket_priority(match):
  return 0

def get_round_priority(match_round, average_round):
  scale_factor = average_round / match_round
  return scale_factor * round_priority_constant

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