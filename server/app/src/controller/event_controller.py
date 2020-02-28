from .. import db, ma
from app.src.controller import get_user_from_auth_header
from app.src.config import key
from ..model.user import User, UserSchema
from ..model.bracket import Bracket, BracketSchema
from ..model.event import Event, EventSchema
from..model.player import Player
from flask import request, jsonify
from flask_restplus import Resource, Namespace
from requests.exceptions import HTTPError
from app.src.controller import xor_crypt_string
from sqlalchemy.exc import IntegrityError
import challonge
import jwt
import pdb
from ..model.tables import Bracket_Players

api = Namespace('event', description='handles CRUD operations for events')

event_schema = EventSchema()
brackets_schema = BracketSchema(many=True)

@api.route('')
class EventController(Resource):
  @api.doc('create a new event')
  def post(self):
    current_user = get_user_from_auth_header(request, api)
    challonge.set_credentials(current_user.challonge_username, xor_crypt_string(current_user.api_key, decode=True))

    try:
      event_name = request.json['event_name']
      # get the brackets from the request, create bracket objects and store them in a list
      brackets_from_request = request.json['brackets']
      list_of_brackets = get_brackets_from_request(brackets_from_request)
      # for each bracket get the list of players from challonge, create player objects and store them in a dictionary
      for bracket in list_of_brackets:
        get_players_from_bracket(bracket)
        # update bracket info
        #bracket.number_of_players =  len(list_of_players)
        #pdb.set_trace()
      # create the event
      event = Event(event_name, current_user.id)
      # add event to database
      db.session.add(event)
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
    
    try:
      event.name = request.json['event_name']
      brackets_from_request = request.json['brackets']
      list_of_brackets = get_brackets_from_request(brackets_from_request)
      brackets_json = brackets_schema.jsonify(list_of_brackets).json
      event.brackets = brackets_json
      db.session.commit()
      return event_schema.jsonify(event)
    except KeyError as e:
      message = f'Missing field on event entity: {e.args[0]}'
      api.abort(400, message)
    except HTTPError as e:
      api.abort(401, 'Invalid credentials.')
    
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
    bracket_players = Bracket_Players(name = participant['name'])
    bracket_players.player = new_player
    bracket_players.bracket = bracket
    bracket.players.append(bracket_players)
    db.session.add(bracket_players)
    db.session.commit()

def get_players_in_both_brackets(players_by_bracket):
  list_of_players = []
  players_in_bracket1 = players_by_bracket[0]
  players_in_bracket2 = players_by_bracket[1]
  # compare each player in bracket 1 to each player in bracket 2 by name only
  for b1 in players_in_bracket1:
    for b2 in players_in_bracket2:
      if b1.name == b2.name:
        list_of_players.append(b1)
  return list_of_players

    
  
