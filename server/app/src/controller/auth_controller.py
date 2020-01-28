from .. import db, ma
from ..model.user import UserSchema
from ..model.user import User
from flask import request, jsonify, make_response
from flask_restplus import Resource, Namespace
from werkzeug.security import check_password_hash

import jwt
import datetime

api = Namespace('auth', description='auth related functionality')

# init schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@api.route('')
class LoginController(Resource):
    @api.doc('user login')
    def post(self):
        auth = request.authorization
        username = auth.username
        password = auth.password
        user = User.query.filter_by(
                username=username
            ).first()
        if user:
            if check_password_hash(user.password, password):
                auth_token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'my_secret_key')
                if auth_token:
                    return jsonify({'token' : auth_token.decode('UTF-8')})
                else:
                    api.abort(404, 'Token could not be generated.')
            else:
                api.abort(404, 'Password is incorrect.')
        else:
            api.abort(404, 'User does not exist.')