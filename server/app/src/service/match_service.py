import challonge
from ..model.match import Match
from ..model.player import Player
from ..model.tables import ChallongePlayer

def get_highest_priority_matches(event, bracket):
  list_of_matches = challonge.matches.index(bracket.bracket_id, state='open')
  return list_of_matches[:bracket.number_of_setups]

def create_match_objects(list_of_match_data, bracket):
  list_of_matches = []
  id = 1
  for match_data in list_of_match_data:
    challonge_player1 = ChallongePlayer.query.filter_by(challonge_id=match_data['player1_id']).first()
    challonge_player2 = ChallongePlayer.query.filter_by(challonge_id=match_data['player2_id']).first()

    match = Match(id, challonge_player1.player_id, challonge_player2.player_id, match_data['round'], bracket.id, bracket.game_name)
    id += 1
    list_of_matches.append(match)
  return list_of_matches
