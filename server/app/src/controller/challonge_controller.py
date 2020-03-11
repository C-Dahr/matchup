from .. import db, ma
from ..model.user import UserSchema, User
from ..model.bracket import Bracket
from ..model.event import Event
from ..service.match_service import determine_priority_for_matches, get_highest_priority_matches
from flask import request, jsonify
from flask_restplus import Resource, Namespace
from app.src.controller import get_user_from_auth_header
from app.src.controller import xor_crypt_string
from requests.exceptions import HTTPError

import requests
import challonge

api = Namespace('challonge', description='challonge related functionality')

@api.route('/brackets')
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

@api.route('/matches/<event_id>')
class MatchController(Resource):
  @api.doc('get matches for an event')
  def get(self, event_id):
    current_user = get_user_from_auth_header(request, api)
    event = Event.query.get(event_id)
    if not event:
      api.abort(404, 'Event not found')

    try:
      challonge.set_credentials(current_user.challonge_username, xor_crypt_string(current_user.api_key, decode=True))

      available_matches = []
      bracket_setups = {}
      for bracket in event.brackets:
        list_of_matches = challonge.matches.index(bracket.bracket_id, state='open')
        matches_not_in_progress = list(filter(lambda match: match['underway_at'] == None, list_of_matches))
        number_of_setups_in_use = len(list_of_matches) - len(matches_not_in_progress)
        
        matches_for_bracket = determine_priority_for_matches(matches_not_in_progress, bracket)

        available_matches = available_matches + matches_for_bracket
        bracket_setups[bracket.id] = bracket.number_of_setups - number_of_setups_in_use

      # sort matches by priority (descending)
      sorted_matches = sorted(available_matches, key=lambda match: match['priority'], reverse=True)

      matches_called = get_highest_priority_matches(sorted_matches, bracket_setups)
      return jsonify(matches_called)
    except HTTPError as e:
      api.abort(401, 'Invalid credentials.')

@api.route('/match/start')
class MatchProgressController(Resource):
  @api.doc('mark a match as in progress')
  def put(self):
    current_user = get_user_from_auth_header(request, api)
    event_id = request.json['event_id']
    event = Event.query.get(event_id)
    if not event:
      api.abort(404, 'Event not found')
    if event not in current_user.events:
      api.abort(401, 'Current user cannot edit this event.')

    match_id = request.json['match_id']
    bracket_id = request.json['bracket_id']
    bracket_challonge_id = Bracket.query.get(bracket_id).bracket_id
    challonge_path = f'https://api.challonge.com/v1/tournaments/{bracket_challonge_id}/matches/{match_id}/mark_as_underway.json'

    response = requests.post(challonge_path)
    return response
