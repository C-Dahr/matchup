from .. import db, ma
from ..model.user import UserSchema, User
from ..model.event import EventSchema, Event
from flask import request, jsonify
from flask_restplus import Resource, Namespace
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError
from app.src.controller import get_user_from_auth_header
from app.src.controller import xor_crypt_string

api = Namespace('user', description='user related operations')

user_not_found = 'User not found.'

# init schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)

events_schema = EventSchema(many=True)

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

    api_key = xor_crypt_string(user.api_key, decode=True)
    user.api_key = api_key
    return user_schema.jsonify(user)
    
  @api.doc('update a user')
  def put(self):
    user = get_user_from_auth_header(request, api)
    
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
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

@api.route('/password')
class UserPasswordController(Resource):
  @api.doc('edit password')
  def put(self):
    current_password = request.json['current_password']
    new_password = request.json['new_password']
    hashed_new_password = generate_password_hash(new_password, method='sha256')
    user = get_user_from_auth_header(request, api)

    if check_password_hash(user.password, current_password):
      user.password = hashed_new_password
      db.session.commit()
    else:
      api.abort(401, 'Incorrect password.')

@api.route('/all')
class UserListController(Resource):
  @api.doc('list of users')
  def get(self):
    users = User.query.all()
    return users_schema.jsonify(users)

@api.route('/events')
class EventListController(Resource):
  @api.doc('get a list of all events the user owns')
  def get(self):
    user = get_user_from_auth_header(request, api)
    return events_schema.jsonify(user.events)
