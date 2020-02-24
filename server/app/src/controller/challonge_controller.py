from .. import db, ma
from ..model.user import UserSchema
from ..model.user import User
from flask import request, jsonify
from flask_restplus import Resource, Namespace
from app.src.controller import get_user_from_auth_header
from app.src.controller import xor_crypt_string
from requests.exceptions import HTTPError

import challonge

api = Namespace('challonge', description='challonge related functionality')

@api.route('')
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


