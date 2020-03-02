import challonge
from .. import db
from ..model.bracket import Bracket
from ..model.player import Player
from ..model.tables import BracketPlayers, ChallongePlayer

def get_brackets_from_request(brackets_from_request, event):
  list_of_brackets = []
  for bracket in brackets_from_request:
    bracket_info = challonge.tournaments.show(bracket['bracket_id'])
    new_bracket = Bracket(bracket_info['id'], event.id, 'challonge',
                          bracket_info['game_name'], bracket['number_of_setups'])
    list_of_brackets.append(new_bracket)
    db.session.add(new_bracket)
  db.session.commit()
  return list_of_brackets

def get_players_from_bracket(bracket):
  # this call to challonge returns a list of dictionaries
  list_of_participants = challonge.participants.index(bracket.bracket_id)
  for participant in list_of_participants:
    new_player = Player()
    db.session.add(new_player)
    db.session.commit()
    new_challonge_player = ChallongePlayer(new_player.id, participant['id'])
    db.session.add(new_challonge_player)
    bracket_players = BracketPlayers(name = participant['name'])
    bracket_players.player = new_player
    bracket_players.bracket = bracket
    bracket.players.append(bracket_players)
    db.session.add(bracket_players)
  db.session.commit()

def get_duplicate_players(list_of_brackets):
  for player1 in list_of_brackets[0].players:
    for player2 in list_of_brackets[1].players:
      if player1.name == player2.name:
        players = (player1.player, player2.player)
        merge_players(players, list_of_brackets)

def merge_players(players, list_of_brackets):
  player1, player2 = players
  challonge_player1_old = player1.challonge_players[0]
  challonge_player2_old = player2.challonge_players[0]
  bracket1 = list_of_brackets[0]
  bracket2 = list_of_brackets[1]
  bracket_player1_old = BracketPlayers.query.get({'player_id':player1.id, 'bracket_id':bracket1.id})
  bracket_player2_old = BracketPlayers.query.get({'player_id':player2.id, 'bracket_id':bracket2.id})
  # create a new player
  merged_player = Player()
  db.session.add(merged_player)
  db.session.commit()
  challonge_player1 = ChallongePlayer(merged_player.id, challonge_player1_old.challonge_id)
  challonge_player2 = ChallongePlayer(merged_player.id, challonge_player2_old.challonge_id)
  # make same relationships
  bracket_player1 = BracketPlayers(name = bracket_player1_old.name)
  bracket_player1.player = merged_player
  bracket_player1.bracket = bracket1
  bracket_player2 = BracketPlayers(name = bracket_player2_old.name)
  bracket_player2.player = merged_player
  bracket_player2.bracket = bracket2
  bracket1.players.append(bracket_player1)
  bracket2.players.append(bracket_player2)
  # add all new entities to db
  db.session.add(bracket_player1)
  db.session.add(bracket_player2)
  db.session.add(challonge_player1)
  db.session.add(challonge_player2)
  db.session.commit()
  # delete all old entities from db
  db.session.delete(challonge_player1_old)
  db.session.delete(challonge_player2_old)
  db.session.delete(bracket_player1_old)
  db.session.delete(bracket_player2_old)
  db.session.delete(player1)
  db.session.delete(player2)
  db.session.commit()

def update_number_of_setups_in_brackets(brackets_from_request, event):
  event_id = event.id
  for bracket in brackets_from_request:
    bracket_object = Bracket.query.filter_by(event_id=event_id, bracket_id=bracket['bracket_id']).first()
    bracket_object.number_of_setups = bracket['number_of_setups']
  db.session.commit()
