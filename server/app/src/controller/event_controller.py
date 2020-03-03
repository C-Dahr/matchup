from .. import db, ma
from app.src.controller import get_user_from_auth_header
from app.src.config import key
from ..model.event import Event, EventSchema
from..model.player import Player
from flask import request, jsonify
from flask_restplus import Resource, Namespace
from requests.exceptions import HTTPError
from app.src.controller import xor_crypt_string
from sqlalchemy.exc import IntegrityError
import challonge
import jwt
<<<<<<< HEAD
import pdb
from ..model.tables import BracketPlayers, ChallongePlayer
=======
from ..service.event_service import *
>>>>>>> b4661eb78146268c229c5c2b52cf79ba7618c083

api = Namespace('event', description='handles CRUD operations for events')

event_schema = EventSchema()

@api.route('')
class EventController(Resource):
  @api.doc('create a new event')
  def post(self):
    current_user = get_user_from_auth_header(request, api)
    challonge.set_credentials(current_user.challonge_username, xor_crypt_string(current_user.api_key, decode=True))

    try:
      event_name = request.json['event_name']
<<<<<<< HEAD
      # get the brackets from the request, create bracket objects and store them in a list
      brackets_from_request = request.json['brackets']
      list_of_brackets = get_brackets_from_request(brackets_from_request)
      # for each bracket get the list of players from challonge, create player objects and store them in a dictionary
      for bracket in list_of_brackets:
        get_players_from_bracket(bracket)
        # update bracket info
        bracket.number_of_players = len(bracket.players)
      # create the event
      event = Event(event_name, current_user.id)
      get_duplicate_players(list_of_brackets)
      # add event to database
=======
      event = Event(event_name, current_user.id)
>>>>>>> b4661eb78146268c229c5c2b52cf79ba7618c083
      db.session.add(event)
      db.session.commit()

      brackets_from_request = request.json['brackets']
      list_of_brackets = get_brackets_from_request(brackets_from_request, event)
      
      for bracket in list_of_brackets:
        get_players_from_bracket(bracket)
        bracket.number_of_players = len(bracket.players)

      get_duplicate_players(list_of_brackets)

      db.session.commit()
      return event_schema.jsonify(event)
    except KeyError as e:
      message = f'Missing field: {e.args[0]}'
      api.abort(400, message)
    except HTTPError as e:
      api.abort(401, 'Invalid credentials.')
  
  @api.doc('update event')
  def put(self):
    current_user = get_user_from_auth_header(request, api)
    challonge.set_credentials(current_user.challonge_username, xor_crypt_string(current_user.api_key, decode=True))
    event = Event.query.filter_by(event_name=request.json['event_name'],user_id=current_user.id).first()
    if not event:
      api.abort(404, 'Event not found')
    
<<<<<<< HEAD
def get_brackets_from_request(brackets_from_request):
  list_of_brackets = []
  for bracket in brackets_from_request:
    bracket_info = challonge.tournaments.show(bracket['bracket_id'])
    new_bracket = Bracket(bracket_info['id'],
                          'challonge',
                          bracket_info['game_name'],
                          bracket['number_of_setups'])
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

    
  
=======
    try:
      event.name = request.json['event_name']
      brackets_from_request = request.json['brackets']

      update_number_of_setups_in_brackets(brackets_from_request, event)
      
      db.session.commit()
      return event_schema.jsonify(event)
    except KeyError as e:
      message = f'Missing field on event entity: {e.args[0]}'
      api.abort(400, message)
    except HTTPError as e:
      api.abort(401, 'Invalid credentials.')
>>>>>>> b4661eb78146268c229c5c2b52cf79ba7618c083
