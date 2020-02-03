from .. import db, ma
from ..model.user import UserSchema
from ..model.user import User
from flask import request, jsonify
from flask_restplus import Resource, Namespace

import challonge
import jwt

api = Namespace('challonge', description='challonge related functionality')

@api.route('')
class BracketController(Resource):
    @api.doc('get brackets')
    def get(self):
        username = request.json['username']
        api_key = request.json['api_key']

        try:
            # set the credentials for interfacing with challonge
            challonge.set_credentials(username, api_key)
            # index returns a list of the user's tournaments
            tournaments = challonge.tournaments.index()
            return jsonify({'tournaments' : tournaments})
        except Exception as e:
            api.abort(401, 'Invalid credentials.')
