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
        # check header for auth token
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            api.abort(404, 'No user signed in.')
        # decode token and get user
        data = jwt.decode(token, 'my_secret_key')
        current_user = User.query.filter_by(id=data['id']).first()
        if not current_user:
            api.abort(404, 'Invalid token.')

        try:
            # set the credentials for interfacing with challonge
            challonge.set_credentials(username, current_user.api_key)
        except Exception as e:
            api.abort(401, 'Invalid credentials.')
        
        # index returns a list of the user's tournaments
        tournaments = challonge.tournaments.index()
        return jsonify({'tournaments' : tournaments})
