from .. import db, ma
from ..model.user import UserSchema
from ..model.user import User
from flask import request, jsonify
from flask_restplus import Resource, Namespace

from project.server import bcrypt, db

api = Namespace('auth', description='auth related functionality')

# init schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@api.route('')
class LoginController(Resource):
    @api.doc('user login')
    def post(self):
        post_username = request.json['username']
        post_password = request.json['password']
        user = User.query.filter_by(
                username=post_username
            ).first()
        if user and bcrypt.check_password_hash(
                user.password, post_password
        ):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 200
        else:
            api.abort(404, 'User does not exist.')