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
        merge_players(player1.player, player2.player, list_of_brackets)

def merge_players(player1, player2, list_of_brackets):
  merged_player = create_player()
  update_challonge_players(player1, player2, merged_player)
  update_player_relationships(list_of_brackets, player1, player2, merged_player)

  db.session.delete(player1)
  db.session.delete(player2)
  db.session.commit()

def create_player():
  merged_player = Player()
  db.session.add(merged_player)
  db.session.commit()
  return merged_player

def update_challonge_players(player1, player2, merged_player):
  old_challonge_player1 = player1.challonge_players[0]
  old_challonge_player2 = player2.challonge_players[0]
  new_challonge_player1 = ChallongePlayer(merged_player.id, old_challonge_player1.challonge_id)
  new_challonge_player2 = ChallongePlayer(merged_player.id, old_challonge_player2.challonge_id)

  db.session.add(new_challonge_player1)
  db.session.add(new_challonge_player2)
  db.session.delete(old_challonge_player1)
  db.session.delete(old_challonge_player2)
  db.session.commit()

def update_player_relationships(list_of_brackets, player1, player2, merged_player):
  bracket1 = list_of_brackets[0]
  bracket2 = list_of_brackets[1]
  old_bracket_player1 = BracketPlayers.query.get({'player_id':player1.id, 'bracket_id':bracket1.id})
  old_bracket_player2 = BracketPlayers.query.get({'player_id':player2.id, 'bracket_id':bracket2.id})
  
  # create new bracket players
  new_bracket_player1 = BracketPlayers(name = old_bracket_player1.name)
  new_bracket_player1.player = merged_player
  new_bracket_player1.bracket = bracket1

  new_bracket_player2 = BracketPlayers(name = old_bracket_player2.name)
  new_bracket_player2.player = merged_player
  new_bracket_player2.bracket = bracket2

  bracket1.players.append(new_bracket_player1)
  bracket2.players.append(new_bracket_player2)
  db.session.add(new_bracket_player1)
  db.session.add(new_bracket_player2)

  # delete old bracket players
  db.session.delete(old_bracket_player1)
  db.session.delete(old_bracket_player2)

  db.session.commit()
