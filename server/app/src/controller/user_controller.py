from .. import db, ma
from ..model.user import UserSchema
from ..model.user import User
from flask import request, jsonify
from flask_restplus import Resource, Namespace
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from app.src.controller import get_user_from_auth_header
from app.src.controller import xor_crypt_string

api = Namespace('user', description='user related operations')

# init schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)

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
      api_key = xor_crypt_string(request.json['api_key'], encode=True)
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
    user = get_user_from_auth_header(request, api)
    if not user:
      api.abort(404, user_not_found)
    return user_schema.jsonify(user)
    
  @api.doc('update a user')
  def put(self):
    user = get_user_from_auth_header(request, api)
    if not user:
      api.abort(404, user_not_found)
    
    try:
      user.username = request.json['username']
      user.challonge_username = request.json['challonge_username']
      user.email = request.json['email']
      user.api_key = xor_crypt_string(request.json['api_key'], encode=True)
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
    user = get_user_from_auth_header(request, api)
    if not user:
      api.abort(404, user_not_found)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

@api.route('/all')
class UserListController(Resource):
  @api.doc('list of users')
  def get(self):
    users = User.query.all()
    return users_schema.jsonify(users)

user_not_found = 'User not found.'
