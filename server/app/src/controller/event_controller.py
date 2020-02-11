from .. import db, ma
from ..model.user import UserSchema
from ..model.user import User
from ..model.bracket import Bracket
from ..model.bracket import BracketSchema
from flask import request, jsonify
from flask_restplus import Resource, Namespace
from server.app.src.controller import get_user_from_auth_header
from request.exceptions import HTTPError
import challonge

import challonge
import jwt
from app.src.config import key

api = Namespace('event', description='handles CRUD operations for events')

@api.route('')
class EventController(Resource):
  # request: {
    #   "event_name": "name",
    #   "brackets": [
    #     {
    #       "bracket_id": 1234,
    #       "number_of_setups": 7
    #     },
    #     {
    #       "bracket_id": 5678,
    #       "number_of_setups": 8
    #     }
    #   ]
    # }

  @api.doc('create a new event')
  def post(self):
    current_user = get_user_from_auth_header(request)
    challonge.set_credentials(current_user.challonge_username, current_user.api_key)

    try:
      event_name = request.json['event_name']
      brackets_from_request = request.json['brackets']
      list_of_brackets = get_brackets_from_request(brackets_from_request)
      event = Event(event_name, current_user.id, list_of_brackets)
      db.session.add(event)
      db.session.commit()
    except KeyError as e:
      message = f'Missing field: {e.args[0]}'
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

  # set_of_players_in_both_brackets = list_of_sets_of_players[0] & list_of_sets_of_players[1]
  # players_only_in_bracket_1 = list_of_sets_of_players[0] - set_of_players_in_both_brackets
  # players_only_in_bracket_2 = list_of_sets_of_players[1] - set_of_players_in_both_brackets

  return list_of_brackets

# def build_set_of_player_names(bracket_participants):
#   set_of_players = set()
#   for player in bracket_participants:
#     set_of_players.add(player['name'])
#   return set_of_players

