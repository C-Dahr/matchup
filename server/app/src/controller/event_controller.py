from .. import db, ma
from ..model.user import User, UserSchema
from ..model.bracket import Bracket, BracketSchema
from ..model.event import Event, EventSchema
from flask import request, jsonify
from flask_restplus import Resource, Namespace
from app.src.controller import get_user_from_auth_header
from requests.exceptions import HTTPError
import challonge

import challonge
import jwt
from app.src.config import key

api = Namespace('event', description='handles CRUD operations for events')

event_schema = EventSchema()
brackets_schema = BracketSchema(many=True)

@api.route('')
class EventController(Resource):
  @api.doc('create a new event')
  def post(self):
    current_user = get_user_from_auth_header(request, api)
    challonge.set_credentials(current_user.challonge_username, current_user.api_key)

    try:
      event_name = request.json['event_name']
      brackets_from_request = request.json['brackets']
      import pdb; pdb.set_trace()
      list_of_brackets = get_brackets_from_request(brackets_from_request)
      brackets_json = brackets_schema.jsonify(list_of_brackets)

      event = Event(event_name, current_user.id, brackets_json)
      db.session.add(event)
      db.session.commit()
      return event_schema.jsonify(event)
    except KeyError as e:
      message = f'Missing field: {e.args[0]}'
      api.abort(400, message)
    except Exception as e:
      
      api.abort(400, 'halp')
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
  return list_of_brackets
