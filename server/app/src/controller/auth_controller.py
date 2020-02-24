from .. import db, ma
from ..model.user import UserSchema
from ..model.user import User
from flask import request, jsonify, make_response
from flask_restplus import Resource, Namespace
from werkzeug.security import check_password_hash

import jwt
import datetime
from app.src.config import key

api = Namespace('auth', description='auth related functionality')

@api.route('')
class LoginController(Resource):
  @api.doc('user login')
  def post(self):
    auth = request.authorization
    username = auth.username
    password = auth.password
    user = User.query.filter_by(username=username).first()
    if user:
      if check_password_hash(user.password, password):
        auth_token = jwt.encode({'id' : user.id}, key)
        if auth_token:
          return jsonify({'token' : auth_token.decode('UTF-8')})
        else:
          api.abort(500, 'Token could not be generated.')
      else:
        api.abort(401, 'Incorrect password.')
    else:
      api.abort(401, 'User could not be found.')