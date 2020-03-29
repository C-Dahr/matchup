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
    except IntegrityError as e:
      message = 'Bracket already in use by another event.'
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
  
  def delete(self):
    current_user = get_user_from_auth_header(request, api)
    event = Event.query.get(request.json['event_id'])
    if not event:
      api.abort(404, 'Event not found')
    if event not in current_user.events:
      api.abort(401, 'Current user cannot access this event.')
    
    player_ids_to_delete = get_player_ids_to_delete(event.brackets[0], event.brackets[1])
    
    delete_challonge_players(event.brackets[0].bracket_id, event.brackets[1].bracket_id)
    delete_bracket_players(event.brackets[0].id, event.brackets[1].id)
    delete_brackets(event.id)
    delete_players_by_id(player_ids_to_delete)
    
    db.session.delete(event)
    db.session.commit()

@api.route('/players')
class PlayerController(Resource):
  @api.doc('return list of players')
  def get(self):
    current_user = get_user_from_auth_header(request, api)
    event = Event.query.get(request.json['event_id'])
    if not event:
      api.abort(404, 'Event not found.')
    if event not in current_user.events:
      api.abort(401, 'Current user cannot access this event.')

    players_in_bracket_1, players_in_both_brackets = get_unique_players(event.brackets[0])
    players_in_bracket_2, players_in_both_brackets = get_unique_players(event.brackets[1])
    combined_players_list = get_combined_players_list(event.brackets, players_in_bracket_1, players_in_bracket_2, players_in_both_brackets)

    return jsonify(combined_players_list)

  @api.doc('merge players')
  def post(self):
    current_user = get_user_from_auth_header(request, api)
    event = Event.query.get(request.json['event_id'])
    if not event:
      api.abort(404, 'Event not found.')
    if event not in current_user.events:
      api.abort(401, 'Current user cannot access this event.')

    players_from_request = request.json['players']

    valid_players = get_valid_players_to_merge(event, players_from_request, api)
    
    for player1, player2 in valid_players:
      list_of_brackets = [player1.bracket, player2.bracket]
      merge_players(player1.player, player2.player, list_of_brackets)
