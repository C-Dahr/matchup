from .. import db, ma
from ..model.user import UserSchema
from ..model.user import User
from flask import request, jsonify
from flask_restplus import Resource, Namespace
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

import jwt
from app.src.config import key

api = Namespace('user', description='user related operations')

# init schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)

#helper method(s)
def get_user_from_auth_header(request):
  # check header for auth token
  if 'x-access-token' in request.headers:
    token = request.headers['x-access-token']
  if not token:
    api.abort(401, 'No user signed in.')
  # decode token and get user
  try:
    data = jwt.decode(token, key)
    current_user = User.query.filter_by(id=data['id']).first()
  except jwt.DecodeError as e:
    api.abort(401, 'Invalid token.')
  if not current_user:
      api.abort(401, 'Invalid token.')
  return current_user

@api.route('')
class UserController(Resource):
  @api.doc('add a new user')
  def post(self):
    try:
      username = request.json['username']
      password = request.json['password']
      hashed_password = generate_password_hash(password, method='sha256')
      challonge_username = request.json['challonge_username']
      email = request.json['email']
      api_key = request.json['api_key']
      new_user = User(username, hashed_password, email, challonge_username, api_key)
      db.session.add(new_user)
      db.session.commit()
      return user_schema.jsonify(new_user)
    except KeyError as e:
      message = f'Missing field on user entity: {e.args[0]}'
      api.abort(400, message)
    except IntegrityError as e:
      message = e.args[0].split('\n')[1]
      api.abort(409, message)

  @api.doc('get a user')
  def get(self):
    user = get_user_from_auth_header(request)
    if not user:
      api.abort(404, user_not_found)
    return user_schema.jsonify(user)
    
  @api.doc('update a user')
  def put(self):
    user = get_user_from_auth_header(request)
    if not user:
      api.abort(404, user_not_found)
    
    try:
      user.username = request.json['username']
      user.password = request.json['password']
      user.challonge_username = request.json['challonge_username']
      user.email = request.json['email']
      user.api_key = request.json['api_key']
      db.session.commit()
      return user_schema.jsonify(user)
    except KeyError as e:
      message = f'Missing field on user entity: {e.args[0]}'
      api.abort(400, message)
    except IntegrityError as e:
      message = e.args[0].split('\n')[1]
      api.abort(409, message)

  @api.doc('delete a user')
  def delete(self):
    user = get_user_from_auth_header(request)
    if not user:
      api.abort(404, user_not_found)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

user_not_found = 'User not found.'
