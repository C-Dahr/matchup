from .. import db, ma
from ..model.user import UserSchema, User
from ..model.event import Event
from ..service.match_service import get_highest_priority_matches
from flask import request, jsonify
from flask_restplus import Resource, Namespace
from app.src.controller import get_user_from_auth_header
from app.src.controller import xor_crypt_string
from requests.exceptions import HTTPError

import challonge

api = Namespace('challonge', description='challonge related functionality')

@api.route('/bracket')
class BracketController(Resource):
  @api.doc('get brackets')
  def get(self):
    current_user = get_user_from_auth_header(request, api)
    try:
      # set the credentials for interfacing with challonge
      challonge.set_credentials(current_user.challonge_username, xor_crypt_string(current_user.api_key, decode=True))
      # index returns a list of the user's tournaments
      tournaments = challonge.tournaments.index()
      return jsonify({'tournaments' : tournaments})
    except HTTPError as e:
      api.abort(401, 'Invalid credentials.')

@api.route('/match/<event_name>')
class MatchController(Resource):
  @api.doc('get matches for an event')
  def get(self, event_name):
    current_user = get_user_from_auth_header(request, api)
    event = Event.query.get({'event_name': event_name, 'user_id': current_user.id})
    try:
      challonge.set_credentials(current_user.challonge_username, xor_crypt_string(current_user.api_key, decode=True))
      bracket_1_matches = get_highest_priority_matches(event, event.brackets[0])
      bracket_2_matches = get_highest_priority_matches(event, event.brackets[1])
      matches = bracket_1_matches + bracket_2_matches
      return jsonify({'matches' : matches})
    except HTTPError as e:
      api.abort(401, 'Invalid credentials.')
