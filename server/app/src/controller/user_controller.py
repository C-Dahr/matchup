from .. import db, ma
from ..model.user import UserSchema
from ..model.user import User
from flask import request, jsonify
from flask_restplus import Resource, Namespace
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError


api = Namespace('user', description='user related operations')

# init schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@api.route('')
class UserListController(Resource):
  @api.doc('list of users')
  def get(self):
    users = User.query.all()
    return users_schema.jsonify(users)
  
  @api.doc('add a new user')
  def post(self):
    try:
      username = request.json['username']
      password = request.json['password']
      hashed_password = generate_password_hash(password, method='sha256')
      email = request.json['email']
      api_key = request.json['api_key']
      new_user = User(username, hashed_password, email, api_key)
      db.session.add(new_user)
      db.session.commit()
      return user_schema.jsonify(new_user)
    except KeyError as e:
      message = f'Missing field on user entity: {e.args[0]}'
      api.abort(400, message)
    except IntegrityError as e:
      message = e.args[0].split('\n')[1]
      api.abort(409, message)

user_not_found = 'User not found.'

@api.route('/<id>')
@api.param('id', 'The User identifier')
class UserController(Resource):
  @api.doc('get a user')
  def get(self, id):
    user = User.query.get(id)
    if not user:
      api.abort(404, user_not_found)
    return user_schema.jsonify(user)
    
  @api.doc('update a user')
  def put(self, id):
    user = User.query.get(id)
    if not user:
      api.abort(404, user_not_found)
    
    try:
      user.username = request.json['username']
      user.password = request.json['password']
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
  def delete(self, id):
    user = User.query.get(id)
    if not user:
      api.abort(404, user_not_found)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)
