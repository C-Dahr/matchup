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
from ..service.event_service import *

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
      event = Event(event_name, current_user.id)
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
    event = Event.query.get(request.json['event_id'])
    if not event:
      api.abort(404, 'Event not found')
    
    try:
      event.event_name = request.json['event_name']
      brackets_from_request = request.json['brackets']
      event.update_number_of_setups_in_brackets(brackets_from_request)
      
      db.session.commit()
      return event_schema.jsonify(event)
    except KeyError as e:
      message = f'Missing field: {e.args[0]}'
      api.abort(400, message)
    except AttributeError as e:
      api.abort(400, 'Invalid bracket specified.')
    except HTTPError as e:
      api.abort(401, 'Invalid credentials.')

@api.route('/players/merge')
class PlayerController(Resource):
  @api.doc('merge players')
  def post(self):
    current_user = get_user_from_auth_header(request, api)
    event = Event.query.get(request.json['event_id'])
    if not event:
      api.abort(404, 'Event not found.')

    players_from_request = request.json['players']

    players_from_check = check_valid_merge(event, players_from_request, api)
    
    for player1, player2 in players_from_check:
      list_of_brackets = [player1.bracket, player2.bracket]
      merge_players(player1.player, player2.player, list_of_brackets)
