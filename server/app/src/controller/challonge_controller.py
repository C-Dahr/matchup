from .. import db, ma
from ..model.user import UserSchema, User
from ..model.bracket import Bracket
from ..model.event import Event
from ..service.match_service import determine_priority_for_matches, get_highest_priority_matches
from ..service.match_service import calculate_mean_bracket_size
from flask import request, jsonify
from flask_restplus import Resource, Namespace
from app.src.controller import get_user_from_auth_header
from app.src.controller import xor_crypt_string
from requests.exceptions import HTTPError

import json
import challonge

from urllib.parse import urlencode
from urllib.request import Request, HTTPBasicAuthHandler, build_opener
from urllib.error import HTTPError as URLLibHTTPError
from xml.etree import cElementTree as ElementTree

api = Namespace('challonge', description='challonge related functionality')

class ChallongeException(Exception):
  pass

@api.route('/verify')
class VerificationController(Resource):
  @api.doc('Verify challonge credentials')
  def post(self):
    try:
      # set the credentials for interfacing with challonge
      challonge_username = request.json['challonge_username']
      api_key = request.json['api_key']
      challonge.set_credentials(challonge_username, api_key)
      # index returns a list of the user's tournaments
      tournaments = challonge.tournaments.index()
      return jsonify({'tournaments' : tournaments})
    except HTTPError as e:
      api.abort(401, 'Invalid credentials.')

@api.route('/brackets')
class BracketController(Resource):
  @api.doc('get brackets')
  def get(self):
    current_user = get_user_from_auth_header(request, api)
    try:
      challonge.set_credentials(current_user.challonge_username, xor_crypt_string(current_user.api_key, decode=True))
      
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

      average_bracket_size = calculate_mean_bracket_size(event.brackets)

      available_matches = []
      bracket_setups = {}
      for bracket in event.brackets:
        list_of_matches = challonge.matches.index(bracket.bracket_id, state='open')
        matches_not_in_progress = list(filter(lambda match: match['underway_at'] == None, list_of_matches))
        number_of_setups_in_use = len(list_of_matches) - len(matches_not_in_progress)
        
        bracket.bracket_size_ratio = bracket.number_of_players / average_bracket_size

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
    bracket_challonge_id = Bracket.query.get({'id':bracket_id, 'event_id':event_id}).bracket_id
    challonge_path = f'https://api.challonge.com/v1/tournaments/{bracket_challonge_id}/matches/{match_id}/mark_as_underway.json'

    response = send_challonge_request(challonge_path, current_user)
    return get_json_data(response)

def send_challonge_request(challonge_path, current_user):
  data = {} # needed so the Request object is a "POST" request
  req = Request(challonge_path, data)

  # use basic authentication
  user, api_key = current_user.challonge_username, xor_crypt_string(current_user.api_key, decode=True)
  auth_handler = HTTPBasicAuthHandler()
  auth_handler.add_password(
      realm="Application",
      uri=req.get_full_url(),
      user=user,
      passwd=api_key
  )
  opener = build_opener(auth_handler)

  try:
    response = opener.open(req)
  except URLLibHTTPError as e:
    if e.code != 422:
      raise
    # wrap up application-level errors
    doc = ElementTree.parse(e).getroot()
    if doc.tag != "errors":
      raise
    errors = [e.text for e in doc]
    raise ChallongeException(*errors)

  return response

def get_json_data(response):
  encoding = response.info().get_content_charset('utf8')
  return json.loads(response.read().decode(encoding))
